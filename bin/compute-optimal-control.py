import argparse

import dolfin
from dolfin import Constant, as_matrix
import numpy as np

from optipuls.simulation import Simulation
from optipuls.problem import Problem
import optipuls.coefficients as coefficients
import optipuls.material as material
import optipuls.optimization as optimization
from optipuls.time import TimeDomain
from optipuls.space import SpaceDomain


# parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-o', '--output', default='../output')
parser.add_argument('-s', '--scratch', default='numericals')
parser.add_argument('-P_YAG', '--P_YAG')
parser.add_argument('-T', '--T')
args = parser.parse_args()

P_YAG = args.P_YAG
T = args.T


# set dolfin parameters
dolfin.set_log_level(40)
dolfin.parameters["form_compiler"]["quadrature_degree"] = 1


# read the material properties and initialize equation coefficients
dummy_material = material.from_file('materials/dummy.json')
vhc = coefficients.construct_vhc_spline(dummy_material)
kappa_rad = coefficients.construct_kappa_spline(dummy_material, 'rad')
kappa_ax = coefficients.construct_kappa_spline(dummy_material, 'ax')


absorb = 0.135
space_domain = SpaceDomain(0.0025, 0.0002, 0.0005)

time_domain = TimeDomain(T, int(T * 10**4))
laser_pd = (absorb * P_YAG) / (np.pi * space_domain.R_laser**2)

problem = Problem()
problem.time_domain = time_domain
problem.space_domain = space_domain
problem.P_YAG = P_YAG
problem.laser_pd = laser_pd

problem.temp_amb = 295.
problem.implicitness = 1.
problem.convection_coeff = 20.
problem.radiation_coeff = 2.26 * 10**-9
problem.liquidus = 923.0
problem.solidus = 858.0

# optimization parameters
problem.control_ref = np.zeros(time_domain.Nt)
problem.beta_control = 10**2
problem.beta_velocity = 10**18
problem.velocity_max = 0.08
problem.beta_liquidity = 10**12
problem.beta_welding = 10**-2
problem.threshold_temp = 1000.
problem.target_point = dolfin.Point(0, .7 * space_domain.Z)
problem.pow_ = 20

# initialize FEM spaces
problem.V = dolfin.FunctionSpace(space_domain.mesh, "CG", 1)
problem.V1 = dolfin.FunctionSpace(space_domain.mesh, "DG", 0)

problem.theta_init = dolfin.project(problem.temp_amb, problem.V)

vhc.problem = problem
kappa_rad.problem = problem
kappa_ax.problem = problem

problem.vhc = vhc
problem.kappa = lambda theta: as_matrix(
                    [[kappa_rad(theta), Constant(0)],
                     [Constant(0), kappa_ax(theta)]])


control = np.zeros(time_domain.Nt)
simulation = Simulation(problem, control)
descent = optimization.gradient_descent(
        simulation,
        iter_max=100,
        step_init=2**-25,
        tolerance=5*10**-5,
        step_prediction=False)


np.save(args.scratch+f'/{P_YAG}-{T:5.3f}-optimal-control.npy',
        descent[-1].control)
