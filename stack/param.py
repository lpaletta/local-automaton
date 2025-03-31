import numpy as np

error_rate_list = [0.01,0.001]
K_list = [9,15,25,50,100]

param_dict = {
    "T" : 1000,
    "K" : 3,
    "error_rate" : 0.2,
    "meas_error_rate" : 0.2,
    "init_var": "Zeros",
}

option_dict = {
    "error_bool": True,
    "meas_error_bool": True,
    "id_error_rate": True
}

view_dict = {
    "record_var" : "Stack",
    "M": 50,
    "dt": 10
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
    "T_cum_max": 10**7,  #maxmax=10 #usuel=9 #test=<8
    "positive_max": 100 #1000
}