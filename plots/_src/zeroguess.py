import argparse

import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from matplotlib import ticker

from parameters import font
from optenv import parameters

# parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outfile')
args = parser.parse_args()

powers = parameters.zeroguess['powers']
times =  parameters.zeroguess['times']


# controls = [
#         np.load(filename)
#         for filename in parameters.zeroguess['optcontrols']
#         ]

matplotlib.rc('font', **font)

fig = plt.figure()
fig.set_size_inches(6, 5)
gs = fig.add_gridspec(3, 3, hspace=0, wspace=0,
                      width_ratios=times, height_ratios=powers)

axes = gs.subplots(sharex='col', sharey='row')


for ax_triple, P_YAG in zip(axes, powers):
    for ax, T in zip(ax_triple, times):
        control = np.load(f'numericals/zeroguess/{P_YAG}-{T:5.3f}.npy')
        ax.plot(np.linspace(0, T, len(control)), control * P_YAG)
        ax.set_ylim(0, P_YAG)
        ax.set_xlim(0, T)
        if T == min(times):
            ax.xaxis.set_ticks(np.arange(0, T + 0.0001, 0.005))
        else:
            ax.xaxis.set_ticks(np.arange(0.005, T + 0.0001, 0.005))
        if P_YAG == max(powers):
            ax.yaxis.set_ticks(np.arange(0, P_YAG + 1, 500))
        else:
            ax.yaxis.set_ticks(np.arange(500, P_YAG + 1, 500))
        ax.yaxis.set_major_formatter('{x:4.0f} W')
        ax.xaxis.set_major_formatter(lambda x, pos: str(int(x*1000)) + ' ms')

plt.tight_layout()
plt.savefig(args.outfile)
