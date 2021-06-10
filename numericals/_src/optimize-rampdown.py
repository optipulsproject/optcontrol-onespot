import argparse
import json
import re

import numpy as np

from optipuls.simulation import Simulation
from optipuls.optimization import gradient_descent
from optipuls.time import TimeDomain
from optipuls.utils.laser import linear_rampdown

from optenv import parameters 
from optenv.problem import problem


# parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outfile')
args = parser.parse_args()

# parse simulation parameters from the outfile
regex = re.compile(r'\d\d\d\d-\d\d\d\d-\d.\d\d\d-\d.\d\d\d-\d.\d\d\d')
P_YAG, P_YAG_rd, t1, t2, T = \
    (lambda P_YAG_str, P_YAG_rd_str, t1_str, t2_str, T_str:
        (int(P_YAG_str),
         int(P_YAG_rd_str),
         float(t1_str),
         float(t2_str),
         float(T_str)
        )
     ) (*regex.search(args.outfile).group().split('-'))


# initialize time_domain
time_domain = TimeDomain(T, int(T * 10**4))
problem.time_domain = time_domain

# set laser's parameters
absorb = 0.135
laser_pd = (absorb * P_YAG) / (np.pi * problem.space_domain.R_laser**2)
problem.P_YAG = P_YAG
problem.laser_pd = laser_pd

# create initial guess and run optimizer
# we use a lower laser power for the rampdown pulse to give space for optimization
control = (P_YAG_rd / P_YAG) * linear_rampdown(time_domain.timeline, t1, t2)
simulation = Simulation(problem, control)
descent = gradient_descent(simulation, **parameters.gradient_descent)
optimized = descent[-1]

# save the optimal control
np.save(args.outfile, optimized.control)

# prepare the report
report = {
    'P_YAG': optimized.problem.P_YAG,
    'T': optimized.problem.time_domain.T,
    'temp_target_point_max': optimized.temp_target_point_vector.max(),
    'penalty_welding_total': optimized.penalty_welding_total,
    'penalty_velocity_total': optimized.penalty_velocity_total,
    'penalty_liquidity_total': optimized.penalty_liquidity_total,
    'penalty_control_total': optimized.penalty_control_total,
    'penalty_total': optimized.J,
}

# save the report
with open(args.outfile.replace('.npy', '.json'), 'w') as report_file:
    json.dump(report, report_file, indent=4)
