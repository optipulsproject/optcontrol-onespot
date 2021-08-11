import dolfin

from optipuls.problem import Problem
import optipuls.coefficients as coefficients
from optipuls.time import TimeDomain
from optipuls.space import SpaceDomain
import optipuls.material

# set up dolfin
dolfin.set_log_level(40)
dolfin.parameters["form_compiler"]["quadrature_degree"] = 1

# set up the problem
problem = Problem()

problem.space_domain = SpaceDomain(0.0025, 0.0002, 0.0005)

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
problem.V = dolfin.FunctionSpace(problem.space_domain.mesh, "CG", 1)
problem.V1 = dolfin.FunctionSpace(problem.space_domain.mesh, "DG", 0)

# read the material properties and initialize equation coefficients
material = optipuls.material.from_file('optenv/material.json')

vhc, polynomial_mid = coefficients.construct_vhc_spline(material)
kappa_rad = coefficients.construct_kappa_spline(material, 'rad')
kappa_ax = coefficients.construct_kappa_spline(material, 'ax')

problem.vhc = vhc
problem.kappa = (kappa_rad, kappa_ax)

# physical parameters
problem.temp_amb = 295.
problem.implicitness = 1.
problem.convection_coeff = 20.
problem.radiation_coeff = 2.26 * 10**-9
problem.liquidus = material.liquidus
problem.solidus = material.solidus
problem.theta_init = dolfin.project(problem.temp_amb, problem.V)
problem.absorb = 0.135

# time step (used to evaluate Nt), since TimeDomain is not assigned here
problem.dt = 10**-4
