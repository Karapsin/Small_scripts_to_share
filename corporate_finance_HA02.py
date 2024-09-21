from random import uniform
N = 10000000 #number of sims for MC
start_price = 60
u = 1.4
d = 1/1.4

def is_up_move(q = 0.489583):
    return True if uniform(0, 1)<=q else False

def get_PV_of_CF(CF, t, Rf=1.05):
    return CF/(Rf**t)

def simul_oil(start_price = start_price,
              years = 10,
              up_factor = u,
              down_factor= d
    ):

    path = [start_price]*(years + 1)
    for i in range(1, years+1):
        path[i] = path[i-1] * (up_factor if is_up_move() else down_factor)

    return path

def get_dcf(get_optimal_CF):
    prices_path = simul_oil()

    def get_PV(prices, t):
        return get_PV_of_CF(get_optimal_CF(prices[t]), t)

    total_value = sum(
                        [
                          get_PV(prices_path, i)
                          for i
                          in range(1, len(prices_path))
                        ]
                  )
    return total_value

def get_MC_est(get_optimal_CF, sims_num = N):
    return sum([get_dcf(get_optimal_CF) for _ in range(sims_num)]) / sims_num

#########################################################################################
#b
def get_optimal_CF_no_flex(price):
    return 10 * (price - 40)

#10 mln sims may take some time, feel free to lower the number
b_res = get_MC_est(get_optimal_CF_no_flex)

#########################################################################################
#c
def get_optimal_CF_flex(price):
    return 0 if price < 40 else 10 * (price - 40)

#10 mln sims may take some time, feel free to lower the number
c_res = get_MC_est(get_optimal_CF_flex)

#########################################################################################
#d
def get_optimal_CF_higher_capacity(price):
    return 0 if price < 40 else 20 * (price - 40)

#10 mln sims may take some time, feel free to lower the number
higher_capacity_res = get_MC_est(get_optimal_CF_higher_capacity)

#########################################################################################
#e
#here CF actually depends on t
def get_optimal_CF_higher_capacity_flex_invest(price,
                                               t,
                                               increase_capacity,
                                               investment_t
    ):
    capacity = 10 if (increase_capacity and t < investment_t) else 20
    return 0 if price < 40 else capacity * (price - 40)

def get_dcf_modified(get_optimal_CF,
                     invest_price,
                     investment_t
    ):

    prices_path = simul_oil()
    def get_PV(prices, t):
        def get_CF(price, t):
            return get_optimal_CF(price,
                                  t,
                                  increase_capacity = True if prices_path[investment_t] == invest_price else False,
                                  investment_t = investment_t
                    )

        return get_PV_of_CF(get_CF(prices[t], t), t)

    total_value = sum(
                        [
                          get_PV(prices_path, i)
                          for i
                          in range(1, len(prices_path))
                        ]
                  )
    return total_value

def get_MC_est_modified(invest_price,
                        investment_t,
                        sims_num = N,
                        get_optimal_CF = get_optimal_CF_higher_capacity_flex_invest
    ):
    return sum([get_dcf_modified(get_optimal_CF, invest_price, investment_t) for _ in range(sims_num)]) / sims_num


#10 mln sims may take some time, feel free to lower the number
#t = 1
t1_invest_u = get_MC_est_modified(start_price*u, 1)
t1_invest_d = get_MC_est_modified(start_price*d, 1)

#t = 2
t2_invest_uu = get_MC_est_modified(start_price*u*u, 2)
t2_invest_ud = get_MC_est_modified(start_price*d*u, 2)
t2_invest_dd = get_MC_est_modified(start_price*d*d, 2)

print('the value of the oil field:')
print(f' b) no flexibility assumption: {b_res}')
print(f' c) output can be controlled: {c_res}')
print(f' d) capacity can be increased at t=0: {higher_capacity_res}')
print(f' e.1) capacity increased at t=1, up state: {t1_invest_u}')
print(f' e.2) capacity increased at t=1, down state: {t1_invest_d}')
print(f' e.3) capacity increased at t=2, up-up state: {t2_invest_uu}')
print(f' e.4) capacity increased at t=2, up-down state: {t2_invest_ud}')
print(f' e.5) capacity increased at t=2, down-down state: {t2_invest_dd}')