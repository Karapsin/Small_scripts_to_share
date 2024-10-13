import sys
sys.path.append("derivatives_ha2")
from movement_sim_funs import *

def get_MC_estimate(sigma,
                    rho,
                    strike,
                    T,
                    num_sims,
                    per_num,
                    S_0,
                    u_0,
                    kappa,
                    theta,
                    lambda_bar,
                    r
    ):

    def get_price_fin():
        return get_stock_price_path(T=T, per_num=per_num, rho=rho,
                                    S_0=S_0, u_0=u_0, kappa=kappa,
                                    theta=theta, lambda_bar=lambda_bar,
                                    sigma=sigma, r=r
               )[per_num - 1]

    def get_payoff():
        return max(get_price_fin() - strike, 0)

    expected_payoff = sum(get_payoff() for _ in range(num_sims))/num_sims

    print(f"sims for strike {strike} are finished")
    return exp(-r*T) * expected_payoff