import pandas as pd

from param import *
from simulations import *

data = []

path_out = "git/measurement/out/"
path_data = "git/measurement/data/"

param_dict.update(param_sgn_dict)
option_dict.update(option_sgn_dict)
input_dict = param_dict | option_dict | mc_dict

for i in range(len(error_rate_list)):
    input_dict["error_rate"] = error_rate_list[i]
    for j in range(len(meas_error_rate_list)):
        input_dict["meas_error_rate"] = meas_error_rate_list[j]
        for k in range(len(K_list)):
            if input_dict["alg_name"] == "Signal":
                input_dict["K"] = K_list[k]
                input_dict["n"] = input_dict["K"]   
            
            input_dict_merged = dict(zip(list(input_dict.keys()),list(input_dict.values())))
            try:
                file = open(path_output+'data_'+str(i)+'_'+str(j)+'_'+str(k)+'.txt')
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