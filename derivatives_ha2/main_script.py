import sys
sys.path.append("derivatives_ha2")
from MC_sim import *
from BS_implied_vol_search import *
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

num_sims = 10000

T = 0.5
per_num = 150
S_0 = 100
u_0 = 0.01
kappa = 2
theta = 0.01
lambda_bar = 0
r = 0

sigmas_list = [0.225, 0.1, 0.2]
rhos_list = [-0.5, 0, 0.5]
strikes_list = [70, 80, 90, 100, 110, 120, 130]

#sigma, rho, strike
def get_MC_estimate_spec(sigma, rho, strike):
    return get_MC_estimate(sigma = sigma,
                           rho = rho,
                           strike = strike,
                           T = T,
                           num_sims = num_sims,
                           per_num = per_num,
                           S_0 = S_0,
                           u_0 = u_0,
                           kappa = kappa,
                           theta = theta,
                           lambda_bar = lambda_bar,
                           r = r
            )
##############################################################################
#part 1, different rhos, sigma = 0.225
sigma = sigmas_list[0]

res_list = list()
for rho in rhos_list:
    print(f"starting sims for rho {rho}")
    for strike in strikes_list:
        price = get_MC_estimate_spec(sigma = sigma, rho = rho, strike = strike)
        res_list.append((strike, find_vol(price, S_0, strike, T, r), rho))

df = pd.DataFrame(res_list)

plt.figure(figsize=(8,6))
for group in df[2].unique():
    subset = df[df[2] == group]
    plt.plot(subset[0], subset[1], label=f'Group {group}')

plt.xlabel('Strikes')
plt.ylabel('Implied vol')
plt.title('Implied vols by strikes, grouped by rho values')
plt.legend(title='rho values')
plt.grid(True)
plt.savefig('derivatives_ha2//1st_plot.png', dpi=300, bbox_inches='tight')


##############################################################################
#part 2, different sigmas, rho = 0
rho = 0
res_list = list()
for sigma in sigmas_list[1:]:
    print(f"starting sims for sigma {sigma}")
    res_list.extend([(x, get_MC_estimate_spec(sigma = sigma, rho = rho, strike = x), sigma)
                     for x in strikes_list
                    ]
             )

for i in range(len(res_list)):
    strike = res_list[i][0]
    price = res_list[i][1]
    sigma = res_list[i][2]
    impl_vol = find_vol(round(price, 1), S_0, strike, T, r)

    res_list[i] = (strike, sigma, impl_vol)

df = pd.DataFrame(res_list)

plt.figure(figsize=(8,6))
for group in df[1].unique():
    subset = df[df[1] == group]
    plt.plot(subset[0], subset[2], label=f'Group {group}')

plt.xlabel('Strikes')
plt.ylabel('implied vol')
plt.title('Prices by strikes, grouped by sigmas')
plt.legend(title='sigma values')
plt.grid(True)
plt.savefig('derivatives_ha2//2nd_plot.png', dpi=300, bbox_inches='tight')