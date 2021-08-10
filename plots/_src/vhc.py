import argparse

import matplotlib
from matplotlib import pyplot as plt
import numpy as np

from optenv.problem import material
from optenv.problem import vhc, polynomial_mid
from parameters import font


# parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outfile')
args = parser.parse_args()

# get the material setup
solidus = material.solidus
liquidus = material.liquidus
knots = material.knots
heat_capacity = material.heat_capacity
density = material.density

# compute the volumetric heat capacity values
values = [c*d for (c,d,k) in zip(heat_capacity,density,knots)]

# setup the plot
matplotlib.rc('font', **font)

fig, ax = plt.subplots()

fig.set_size_inches(3, 2.25)
plt.yscale('log')

ax.set_xticks(knots)
ax.set_xticklabels(knots, rotation=45)

x = np.linspace(223, 1123, 900)
x_corridor = x[(x > solidus) & (x < liquidus)]


ax.plot(x, np.vectorize(vhc)(x),
        zorder=0,
        color='C0',
        label=r'$s(\theta)$ spline fitting',
)
ax.fill_between(x, polynomial_mid(x), np.vectorize(vhc)(x),
        where=((x > solidus) & (x < liquidus)),
        color='C0',
        zorder=1,
        alpha=0.1,
        label='enthalpy of fusion',
)
ax.scatter(knots, values,
           zorder=1,
           marker='x',
           color='red',
           label='experimental data',
)
ax.legend(loc='upper left')

plt.tight_layout()
plt.savefig(args.outfile)
