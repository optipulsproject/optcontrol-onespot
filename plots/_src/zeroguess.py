import argparse

import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator, AutoMinorLocator

from parameters import font

# parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outfile')
args = parser.parse_args()

powers = [1500, 2000, 2500]
times =  [0.010, 0.015, 0.020]


controls = [
                [np.load(f'numericals/zeroguess/{P_YAG}-{T:5.3f}.npy')
                    for T in times
                ]
                for P_YAG in powers
           ]

matplotlib.rc('font', **font)

fig = plt.figure()
fig.set_size_inches(6, 5)
gs = fig.add_gridspec(3, 3, hspace=0, wspace=0,
                      width_ratios=times, height_ratios=powers)

axes = gs.subplots(sharex='col', sharey='row')


for ax_triple, control_triple in zip(axes, controls):
    for ax, control in zip(ax_triple, control_triple):
        ax.plot(control)
        ax.set_ylim(0, 1.1)

# axes[0,0].yaxis.set_minor_locator(MultipleLocator(3))
# axes[0,0].yaxis.set_major_formatter('{x:1.1f}')

plt.tight_layout()
plt.savefig(args.outfile)
