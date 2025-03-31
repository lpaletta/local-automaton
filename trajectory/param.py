import numpy as np

param_dict = {
    "T" : 50,
    "K" : 5,
    "error_rate" : 0.4,
    "meas_error_rate" : 0,
    "init_var": "Random Error", #{"Zeros", "Random", "Random Error", "Specified"}
}

option_dict = {
    "error_bool": False,
    "meas_error_bool": False,
    "id_error_rate": True
}

view_dict = {
    "record_var" : "Trajectory", #{"Logical", "Data", "Poisson", "Stack", "Trajectory"}
    "dt": 10,
    "M": 50
}

param_sgn_dict = {
    "anti_signal_velocity": 3,
    "backward_signal_velocity": 3,
    "init_data_array": np.array(())
}

option_sgn_dict = {
    "bidirectional_bool": False
}