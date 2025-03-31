import pandas as pd

from param import *
from simulations import *

data = []

path_data = "git/logical/data/"
path_out = "git/logical/out/"

for i in range(len(alg_list)):
    param_dict["alg_name"] = alg_list[i]
    param_dict_copy = param_dict.copy()
    option_dict_copy = option_dict.copy()
    if param_dict_copy["alg_name"] == "Signal":
        param_dict_copy.update(param_sgn_dict)
        option_dict_copy.update(option_sgn_dict)
        input_dict = param_dict_copy | option_dict_copy
        K_list = K_sgn_list
    elif param_dict_copy["alg_name"] == "Toom":
        param_dict_copy.update(param_toom_dict)
        option_dict_copy.update(option_toom_dict)
        input_dict = param_dict_copy | option_dict_copy
        K_list = K_toom_list
    elif param_dict_copy["alg_name"] == "Shearing":
        param_dict_copy.update(param_shearing_dict)
        option_dict_copy.update(option_shearing_dict)
        input_dict = param_dict_copy | option_dict_copy
        K_list = K_shearing_list
    for j in range(len(error_rate_list)):
        input_dict["error_rate"] = error_rate_list[j]

        for k in range(len(K_list)):
            if input_dict["alg_name"] == "Signal":
                input_dict["K"] = K_list[k]
                input_dict["n"] = input_dict["K"]
            elif input_dict["alg_name"] == "Toom":
                input_dict["K"] = K_list[k]
                input_dict["n"] = input_dict["K"]**2
            elif input_dict["alg_name"] == "Shearing":
                input_dict["K"] = K_list[k]
                input_dict["n"] = 2*input_dict["K"]        
            
            input_dict_merged = dict(zip(list(input_dict.keys()),list(input_dict.values())))
            try:
                file = open(path_out+'data_'+str(i)+'_'+str(j)+'_'+str(k)+'.txt')
                output_list_of_string = [s.split(" ") for s in file.readlines()]
                input_dict_merged["positive"] = np.sum([int(output_list_of_string[i][0]) for i in range(len(output_list_of_string))],dtype=int)
                input_dict_merged["number_of_runs"] = np.sum([int(output_list_of_string[i][1]) for i in range(len(output_list_of_string))],dtype=int)
                input_dict_merged["T"] = int(output_list_of_string[0][2])
                data.append(input_dict_merged)
                file.close()
            except:
                pass

df = pd.DataFrame.from_records(data)
df.loc[-1] = df.dtypes
df.sort_index(inplace=True)

df = df[["alg_name","K","n","error_bool","meas_error_bool","error_rate","meas_error_rate","positive","number_of_runs","T"]]

df.to_csv(path_data+"data_from_out.csv",index=False)