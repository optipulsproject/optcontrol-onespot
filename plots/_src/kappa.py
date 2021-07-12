import argparse

import matplotlib
from matplotlib import pyplot as plt
import numpy as np

from optenv.problem import dummy_material as material
from optenv.problem import kappa_rad, kappa_ax
from parameters import font


# parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outfile')
args = parser.parse_args()

# get the material setup
solidus = material.solidus
liquidus = material.liquidus
knots = material.knots[:7]
values = material.kappa_rad[:7]


# setup the plot
matplotlib.rc('font', **font)

fig, ax = plt.subplots()

fig.set_size_inches(3, 2.25)
plt.yscale('log')

ax.set_xticks(knots)
ax.set_xticklabels(knots, rotation=45)

x = np.linspace(223, 1123, 900)
x_solid = x[x <= solidus]
x_notsolid = x[x > solidus]

# experimental data
ax.scatter(knots, values,
           color='red',
           zorder=1,
           marker='x',
           label='experimental data',
)
# linear approximation in the fully solid state
ax.plot(x_solid, np.vectorize(kappa_rad)(x_solid),
        color='C0',
        linestyle=(0, (8, 8)),
        zorder=0,
)
ax.plot(x_solid, np.vectorize(kappa_rad)(x_solid),
        color='C1',
        linestyle=(8, (8, 8)),
        zorder=0,
)
# approximation in not fully solid state (radial)
ax.plot(x_notsolid, np.vectorize(kappa_rad)(x_notsolid),
        color='C0',
        zorder=0,
        label=r'$\kappa_\mathrm{ax}(\theta)$ spline fitting',
)
# approximation in not fully solid state (axial)
ax.plot(x_notsolid, np.vectorize(kappa_ax)(x_notsolid),
        color='C1',
        zorder=0,
        label=r'$\kappa_\mathrm{ax}(\theta)$ spline fitting',
)

ax.legend(loc='upper left')
plt.tight_layout()
plt.savefig(args.outfile)
