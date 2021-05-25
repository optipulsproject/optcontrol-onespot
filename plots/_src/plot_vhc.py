from matplotlib import pyplot as plt
import numpy as np
import optipuls.coefficients as coef

knots = np.array(list(coef.knots_sol) + list(coef.knots_liq))
values = (np.array(list(coef.c_sol) + list(coef.c_liq)) *
          np.array(list(coef.rho_sol) + list(coef.rho_liq)))

vhc_vec = np.vectorize(coef.vhc)
x = np.linspace(223, 1123, 900)

plt.rcParams.update({'font.size': 8})
fig, ax = plt.subplots()

fig.set_size_inches(3, 2.25)

plt.yscale('log')

ax.set_xticks(knots)
ax.set_xticklabels(knots, rotation=45)

ax.plot(x, vhc_vec(x), color='blue', zorder=0,
        label=r'$s(\theta)$ spline fitting')
ax.scatter(knots, values, color='red', zorder=1,
        label='experimental data')
ax.legend(loc='upper left')
plt.tight_layout()
# plt.show()
plt.savefig('vhc.pgf')  
