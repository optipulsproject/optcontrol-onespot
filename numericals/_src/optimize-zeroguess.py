import argparse
import json
import re

import numpy as np

from optipuls.simulation import Simulation
from optipuls.optimization import gradient_descent
from optipuls.time import TimeDomain

from optenv import parameters 
from optenv.problem import problem


# parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outfile')
args = parser.parse_args()

# extract parameters from the file name
regex = re.compile(r'\d\d\d\d-\d.\d\d\d')
P_YAG, T = (lambda si, sf: (int(si), float(sf))) (
                *regex.search(args.outfile).group().split('-'))

# initialize time_domain
time_domain = TimeDomain(T, int(T / problem.dt))
problem.time_domain = time_domain

# set laser's parameters
laser_pd = (problem.absorb * P_YAG) / (np.pi * problem.space_domain.R_laser**2)
problem.P_YAG = P_YAG
problem.laser_pd = laser_pd

# create initial guess and run optimizer
control = np.zeros(time_domain.Nt)
simulation = Simulation(problem, control)
descent = gradient_descent(simulation, **parameters.gradient_descent)
optimized = descent[-1]

np.save(args.outfile, optimized.control)

report = {
    'P_YAG': optimized.problem.P_YAG,
    'T': optimized.problem.time_domain.T,
    'welding_depth_max': optimized.welding_depth_vector.max(),
    'penalty_welding_total': optimized.penalty_welding_total,
    'penalty_velocity_total': optimized.penalty_velocity_total,
    'penalty_liquidity_total': optimized.penalty_liquidity_total,
    'penalty_control_total': optimized.penalty_control_total,
    'penalty_total': optimized.J,
}

with open(args.outfile.replace('.npy', '.json'), 'w') as report_file:
    json.dump(report, report_file, indent=4)
