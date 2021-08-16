import argparse

import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator, AutoMinorLocator

# from optipuls.utils.laser import linear_rampdown
# from optipuls.time import TimeDomain

from parameters import font

import optenv.parameters

# parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outfile')
args = parser.parse_args()

P_YAG = optenv.parameters.rampdown['power_max']
# P_YAG_rd = optenv.parameters.rampdown['power_rampdown']
T = optenv.parameters.rampdown['T']
# t1 = optenv.parameters.rampdown['t1']
# t2s = optenv.parameters.rampdown['t2s']


controls_opt = [
        np.load(filename)
        for filename in optenv.parameters.rampdown['optcontrols']
        ]
controls_noopt = [
        np.load(filename.replace('rampdown', 'rampdown-noopt'))
        for filename in optenv.parameters.rampdown['optcontrols']
        ]

matplotlib.rc('font', **font)

fig, axes = plt.subplots(1, 2)
fig.set_size_inches(5, 2)

for ax, control_opt, control_noopt in zip(axes, controls_opt, controls_noopt):
    ax.plot(
        np.linspace(0, T, len(control_noopt)),
        control_noopt * P_YAG,
        alpha=0.3,
        color='C0',
        zorder=0
        )
    ax.plot(
        np.linspace(0, T, len(control_opt)),
        control_opt * P_YAG,
        color='C0',
        zorder=1,
        )
    ax.set_ylim(0, P_YAG)
    ax.xaxis.set_ticks(np.arange(0, T + 0.0001, 0.004))
    ax.yaxis.set_ticks(np.arange(0, P_YAG + 1, 500))
    ax.yaxis.set_major_formatter('{x:4.0f} W')
    ax.xaxis.set_major_formatter(lambda x, pos: str(int(x*1000)) + ' ms')


plt.tight_layout()
plt.savefig(args.outfile)
