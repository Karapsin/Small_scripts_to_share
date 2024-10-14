import sys
from types import NoneType

sys.path.append("derivatives_ha2")
from MC_sim import *
from BS_implied_vol_search import *
from plot_funs import *
import pandas as pd

params_dict = {"num_sims": 10000,
               "T": 0.5,
               "per_num": 150,
               "S_0": 100,
               "u_0": 0.01,
               "kappa": 2,
               "theta": 0.01,
               "lambda_bar": 0,
               "r": 0
              }

sigmas_list = [0.225, 0.1, 0.2]
rhos_list = [-0.5, 0, 0.5]
strikes_list = [70, 80, 90, 100, 110, 120, 130]

def find_vol_spec(params_dict):
    def search_vol():
        price = get_MC_estimate(params_dict)
        return find_vol(price, params_dict['S_0'], params_dict['strike'], params_dict['T'], params_dict['r'])

    while True:
        try:
            vol = search_vol()
            if vol is None:
                raise ValueError("Implied volatility is None!")
            else:
                break
        except:
            print("Implied volatility is None! Retrying...")
    return vol

##############################################################################
#part 1, different rhos, sigma = 0.225
params_dict['sigma'] = sigmas_list[0]

res_list = list()
for rho in rhos_list:
    print(f"starting sims for rho {rho}")
    for strike in strikes_list:
        params_dict['rho'] = rho
        params_dict['strike'] = strike

        implied_vol = find_vol_spec(params_dict)

        res_list.append((strike, implied_vol, rho))

plot_and_save(df = pd.DataFrame(res_list),
              group_column = 2,
              x_column = 0,
              y_column = 1,
              x_label = "Strikes",
              y_label = "Implied vol",
              title = 'Implied vols by strikes, grouped by rho values',
              legend_text = "rho values",
              file_name = "1st_plot.png"
)


##############################################################################
#part 2, different sigmas, rho = 0
params_dict['rho'] = 0
res_list2 = list()
for sigma in sigmas_list[1:]:
    print(f"starting sims for sigma {sigma}")
    for strike in strikes_list:
        params_dict['sigma'] = sigma
        params_dict['strike'] = strike
        implied_vol = find_vol_spec(params_dict)

        res_list2.append((strike, implied_vol, sigma))

plot_and_save(df = pd.DataFrame(res_list2),
              group_column = 2,
              x_column = 0,
              y_column = 1,
              x_label = "Strikes",
              y_label = "Implied vol",
              title = 'Implied vols by strikes, grouped by sigmas',
              legend_text = "sigma values",
              file_name = "2nd_plot.png"
)