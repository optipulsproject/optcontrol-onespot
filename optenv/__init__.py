'''This module creates a partially initialized Problem instance.

Notice that problem.time_domain and laser's properties must be set before
running optimization routines.

The correct behaviour is guaranteed only when optcontrol-manuscript branch
of optipuls module is checked out.

'''

import dolfin

dolfin.set_log_level(40)
dolfin.parameters["form_compiler"]["quadrature_degree"] = 1
