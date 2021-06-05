import dolfin
from dolfin import Constant, as_matrix

from optipuls.problem import Problem
import optipuls.coefficients as coefficients
import optipuls.material as material
from optipuls.time import TimeDomain
from optipuls.space import SpaceDomain

# set up the problem
problem = Problem()

space_domain = SpaceDomain(0.0025, 0.0002, 0.0005)
problem.space_domain = space_domain

# optimization parameters
problem.beta_control = 10**2
problem.beta_velocity = 10**18
problem.velocity_max = 0.15
problem.beta_liquidity = 10**12
problem.beta_welding = 10**-2
problem.threshold_temp = 1000.
problem.target_point = dolfin.Point(0, .7 * problem.space_domain.Z)
problem.pow_ = 20

# initialize FEM spaces
problem.V = dolfin.FunctionSpace(space_domain.mesh, "CG", 1)
problem.V1 = dolfin.FunctionSpace(space_domain.mesh, "DG", 0)

# read the material properties and initialize equation coefficients
dummy_material = material.from_file('optenv/material.json')

vhc = coefficients.construct_vhc_spline(dummy_material)
kappa_rad = coefficients.construct_kappa_spline(dummy_material, 'rad')
kappa_ax = coefficients.construct_kappa_spline(dummy_material, 'ax')

# let the spline object know about the functional space
# in order to generate a UFL-form
# a dull solution until we have a better one
vhc.problem = problem
kappa_rad.problem = problem
kappa_ax.problem = problem

problem.vhc = vhc
problem.kappa = lambda theta: as_matrix(
                    [[kappa_rad(theta), Constant(0)],
                     [Constant(0), kappa_ax(theta)]])

# physical parameters
problem.temp_amb = 295.
problem.implicitness = 1.
problem.convection_coeff = 20.
problem.radiation_coeff = 2.26 * 10**-9
problem.liquidus = dummy_material.liquidus
problem.solidus = dummy_material.solidus
problem.theta_init = dolfin.project(problem.temp_amb, problem.V)
