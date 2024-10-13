import sys
import numpy as np
from math import sqrt, exp

def rand_norm(means_list, std_list, rho, n):
    return np.random.multivariate_normal(means_list,
                                         [
                                             [std_list[0]**2, rho*std_list[0]*std_list[1]],
                                             [rho*std_list[0]*std_list[1], std_list[1]**2]
                                         ],
                                         n
           )

def get_vol_increment(u_t, dXt, dt, kappa, theta, sigma, lambda_bar):
    return kappa * (theta - u_t) - lambda_bar * sqrt(u_t) * sigma * sqrt(u_t) * dt + sigma * sqrt(u_t) * dXt

def get_stock_increment(dXt, S_t, u_t, dt, r):
    return r * S_t * dt + sqrt(u_t) * S_t * dXt

def get_stock_price_path(T,
                         per_num,
                         rho,
                         S_0,
                         u_0,
                         kappa,
                         theta,
                         lambda_bar,
                         sigma,
                         r
    ):
    dt = T / per_num
    price_path = [S_0] * per_num
    vol_path = [u_0] * per_num

    def get_vol_increment_spec (u_t, dXt):
        return get_vol_increment(u_t = u_t,
                                 dXt = dXt,
                                 dt = dt,
                                 kappa = kappa,
                                 theta = theta,
                                 sigma = sigma,
                                 lambda_bar = lambda_bar
                )

    def get_stock_increment_spec (S_t, u_t, dXt):
        return get_stock_increment(S_t = S_t,
                                   u_t = u_t,
                                   dXt = dXt,
                                   dt = dt,
                                   r = r
                )

    dXt_sims = rand_norm([0, 0], [sqrt(dt), sqrt(dt)], rho, per_num)
    for i in range(1, per_num):
        vol_path[i] = max(vol_path[i - 1] + get_vol_increment_spec(u_t = vol_path[i - 1], dXt = dXt_sims[i][0]), 0)
        price_path[i] = price_path[i - 1] + get_stock_increment_spec(dXt = dXt_sims[i][1], S_t = price_path[i - 1], u_t = vol_path[i - 1])

    return price_path

