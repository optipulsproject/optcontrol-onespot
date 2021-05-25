from matplotlib import pyplot as plt
import numpy as np
import optipuls.coefficients as coef

knots = coef.knots_sol
values = coef.kappa_sol

kappa_rad_vec = np.vectorize(coef.kappa_rad)
kappa_ax_vec = np.vectorize(coef.kappa_ax)
x = np.linspace(223, 1123, 900)

plt.rcParams.update({'font.size': 8})
fig, ax = plt.subplots()

fig.set_size_inches(3, 2.25)

plt.yscale('log')

ax.set_xticks(knots)
ax.set_xticklabels(knots, rotation=45)

ax.plot(x, kappa_rad_vec(x), color='violet', zorder=0,
        label=r'$\kappa_{rad}(\theta)$ spline fitting')
ax.plot(x, kappa_ax_vec(x), color='blue', zorder=0,
        label=r'$\kappa_{ax}(\theta)$ spline fitting')
ax.scatter(knots, values, color='red', zorder=1,
        label='experimental data')
ax.legend(loc='upper left')
plt.tight_layout()
# plt.show()
plt.savefig('kappa.pgf')  
