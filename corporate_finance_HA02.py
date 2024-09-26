from random import uniform
N = 10000000 #number of sims for MC
start_price = 60
u = 1.4
d = 1/1.4
gross_risk_free = 1.05
periods = 10
production_cost = 40
include_zero_cf = True 
include_last_period = False #e.g. 10 periods, if True, we have periods from 0 to 10, else from 0 to 9

def get_PV_of_CF(CF, t, Rf=gross_risk_free):
    return CF/(Rf**t)

def simul_oil(start_price = start_price,
              years = periods,
              up_factor = u,
              down_factor= d,
              include_last_year = include_last_period
    ):
    def is_up_move(q=(gross_risk_free-d)/(u-d)):
        return True if uniform(0, 1) <= q else False

    periods_num = years + 1 if include_last_year else years

    path = [start_price]*periods_num
    for i in range(1, len(path)):
        path[i] = path[i-1] * (up_factor if is_up_move() else down_factor)

    return path

def get_dcf(get_multiplier,
            cost = production_cost,
            include_zero = include_zero_cf
    ):
    global prices_path
    prices_path = simul_oil()

    def get_PV(t):
        global price
        price = prices_path[t]

        global period
        period = t

        return get_PV_of_CF((price - cost)*get_multiplier(), period)

    start_index = 0 if include_zero else 1
    total_value = sum(
                        [
                          get_PV(i)
                          for i
                          in range(start_index, len(prices_path))
                        ]
                  )
    return total_value

def get_MC_est(get_multiplier, sims_num = N):
    return sum([get_dcf(get_multiplier) for _ in range(sims_num)]) / sims_num

#########################################################################################
#b
def get_multiplier_no_flex():
    return 10

#10 mln sims may take some time, feel free to lower the number
b_res = get_MC_est(get_multiplier_no_flex)

#########################################################################################
#c
def get_multiplier_flex():
    return 0 if price < 40 else 10

#10 mln sims may take some time, feel free to lower the number
c_res = get_MC_est(get_multiplier_flex)

#########################################################################################
#d
def get_multiplier_higher_capacity():
    return 0 if price < 40 else 20

#10 mln sims may take some time, feel free to lower the number
higher_capacity_res = get_MC_est(get_multiplier_higher_capacity)

#########################################################################################
#e
#here CF actually depends on t
def get_multiplier_flex_invest(invest_price, invest_t):
    if prices_path[invest_t] == invest_price and period>=invest_t:
        capacity = 20
    else:
        capacity = 10

    return 0 if price < 40 else capacity

from functools import partial
def get_MC_nested(invest_price, invest_t):

    get_mult_spec = partial(get_multiplier_flex_invest,
                            invest_price = invest_price,
                            invest_t = invest_t
                    )

    return get_MC_est(get_mult_spec)

#10 mln sims may take some time, feel free to lower the number
#t = 1
t1_invest_u = get_MC_nested(start_price*u, 1)
t1_invest_d = get_MC_nested(start_price*d, 1)

#t = 2
t2_invest_uu = get_MC_nested(start_price*u*u, 2)
t2_invest_ud = get_MC_nested(start_price*d*u, 2)
t2_invest_dd = get_MC_nested(start_price*d*d, 2)

print('the value of the oil field:')
print(f' b) no flexibility assumption: {b_res}')
print(f' c) output can be controlled: {c_res}')
print(f' d) capacity can be increased at t=0: {higher_capacity_res}')
print(f' e.1) capacity increased at t=1, up state: {t1_invest_u}')
print(f' e.2) capacity increased at t=1, down state: {t1_invest_d}')
print(f' e.3) capacity increased at t=2, up-up state: {t2_invest_uu}')
print(f' e.4) capacity increased at t=2, up-down state: {t2_invest_ud}')
print(f' e.5) capacity increased at t=2, down-down state: {t2_invest_dd}')