import argparse

import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator, AutoMinorLocator

from optipuls.utils.laser import linear_rampdown
from optipuls.time import TimeDomain


from parameters import font


# parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-o', '--outfile')
args = parser.parse_args()

P_YAG = 2000
P_YAG_rd = 1500
T = 0.012
t1 = 0.005
t2_times = [0.005, 0.010]


controls = [np.load(f'numericals/rampdown/{P_YAG}-{P_YAG_rd}-{t1:5.3f}-{t2:5.3f}-{T:5.3f}.npy')
                    for t2 in t2_times]


matplotlib.rc('font', **font)

fig, axes = plt.subplots(1, 2)
fig.set_size_inches(5, 2)

for ax, control, t2 in zip(axes, controls, t2_times):
    ax.plot(
        (P_YAG_rd / P_YAG) * \
            linear_rampdown(TimeDomain(T, len(control)).timeline, t1, t2),
        alpha=0.3,
        color='blue',
        zorder=0
        )
    ax.plot(control, color='blue', zorder=1)
    ax.set_ylim(0, 1)

plt.tight_layout()
plt.savefig(args.outfile)
