import numpy as np

error_rate_list = [0.02]
K_list = [9,15,25,35,50]

param_dict = {
    "T" : 10**5,
    "K" : 3,
    "error_rate" : 0.02,
    "meas_error_rate" : 0.02,
    "init_var": "Zeros",
}

option_dict = {
    "error_bool": True,
    "meas_error_bool": True,
    "id_error_rate": True
}

view_dict = {
    "record_var" : "Poisson",
    "M": 50,
    "dt": param_dict["T"]//1000
}

param_sgn_dict = {
    "anti_signal_velocity": 3,
    "backward_signal_velocity": 3,
    "init_data_array": np.array(())
}

option_sgn_dict = {
    "bidirectional_bool": True
}

mc_dict = {
    "alg_name": "Signal",
    "T_inner_job": 10000,
    "T_cum_max": 10**7,
    "positive_max": 100
}