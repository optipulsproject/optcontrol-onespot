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
parser.add_argument('--opt', dest='optimize', action='store_true')
parser.add_argument('--no-opt', dest='optimize', action='store_false')
parser.set_defaults(optimize=True)
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
time_domain = TimeDomain(T, int(T / problem.dt))
problem.time_domain = time_domain

# set laser's parameters
laser_pd = (problem.absorb * P_YAG) / (np.pi * problem.space_domain.R_laser**2)
problem.P_YAG = P_YAG
problem.laser_pd = laser_pd

# create initial guess and run optimizer
# we use a lower laser power for the rampdown pulse to give space for optimization
control = (P_YAG_rd / P_YAG) * linear_rampdown(time_domain.timeline, t1, t2)
simulation = Simulation(problem, control)

if args.optimize:
    descent = gradient_descent(simulation, **parameters.gradient_descent)
    optimized = descent[-1]
else:
    optimized = simulation

# save the optimal control
np.save(args.outfile, optimized.control)

# prepare the report
if t2 > t1:
    pulse_shape = 'linear rampdown'
else:
    pulse_shape = 'conventional'

if args.optimize:
    pulse_shape += ' *'
report = {
    'pulse_shape': pulse_shape,
    'welding_depth_max': optimized.welding_depth_vector.max(),
    'penalty_welding_total': optimized.penalty_welding_total,
    'penalty_velocity_total': optimized.penalty_velocity_total,
    'penalty_liquidity_total': optimized.penalty_liquidity_total,
    'penalty_control_total': optimized.penalty_control_total,
    'penalty_total': optimized.J,
}

# save the report
with open(args.outfile.replace('.npy', '.json'), 'w') as report_file:
    json.dump(report, report_file, indent=4)
