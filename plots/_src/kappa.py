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

ax.plot(x, np.vectorize(kappa_rad)(x), color='violet', zorder=0,
        label=r'$\kappa_\mathrm{rad}(\theta)$ spline fitting')
ax.plot(x, np.vectorize(kappa_ax)(x), color='blue', zorder=0,
        label=r'$\kappa_\mathrm{ax}(\theta)$ spline fitting')
ax.scatter(knots, values, color='red', zorder=1,
        label='experimental data')
ax.legend(loc='upper left')
plt.tight_layout()
plt.savefig(args.outfile)
