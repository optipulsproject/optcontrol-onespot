import argparse
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
time_domain = TimeDomain(T, int(T * 10**4))
problem.time_domain = time_domain

# set laser's parameters
absorb = 0.135
laser_pd = (absorb * P_YAG) / (np.pi * problem.space_domain.R_laser**2)
problem.P_YAG = P_YAG
problem.laser_pd = laser_pd

# create initial guess and run optimizer
control = np.zeros(time_domain.Nt)
simulation = Simulation(problem, control)
descent = gradient_descent(simulation, **parameters.gradient_descent)

np.save(args.outfile, descent[-1].control)
