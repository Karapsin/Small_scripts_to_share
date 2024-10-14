import sys
sys.path.append("derivatives_ha2")
from movement_sim_funs import *
import numbers
import warnings

def get_MC_estimate(params_dict):

    #checking params
    all_params = {"num_sims", "T", "per_num", "S_0", "u_0", "kappa", "theta", "lambda_bar", "r", "sigma", "rho", "strike"}
    for param in all_params:
        if param not in params_dict:
            raise KeyError(f"param {param} is not specified")
        if not(isinstance(params_dict[param], numbers.Number)):
            raise TypeError(f"param {param} is supposed to be a number")

    if len(params_dict) != len(all_params):
        warnings.warn(f"params {params_dict.keys - all_params} are not known and will not be used", UserWarning)

    def get_payoff():
        stock_fin_price = get_stock_price_path(params_dict)[params_dict['per_num'] - 1]
        return max(stock_fin_price - params_dict['strike'], 0)

    expected_payoff = sum(get_payoff() for _ in range(params_dict['num_sims']))/params_dict['num_sims']

    print(f"sims for strike {params_dict['strike']} are finished")
    return exp(-params_dict['r']*params_dict['T']) * expected_payoff