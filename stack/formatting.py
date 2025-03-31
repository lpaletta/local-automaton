import pandas as pd

from param import *
from simulations import *

data = []

path_out = "git/stack/out/"
path_data = "git/stack/data/"

param_dict.update(param_sgn_dict)
option_dict.update(option_sgn_dict)
input_dict = param_dict | option_dict | mc_dict

for i in range(len(error_rate_list)):
    input_dict["error_rate"] = error_rate_list[i]

    for j in range(len(K_list)):
        if input_dict["alg_name"] == "Signal":
            input_dict["K"] = K_list[j]
            input_dict["n"] = input_dict["K"]
        
        input_dict_merged = dict(zip(list(input_dict.keys()),list(input_dict.values())))
        
        try:
            file = open(path_out+'data_'+str(i)+'_'+str(j)+'.txt')
            output_list_of_string = [s.split(" ") for s in file.readlines()]
            stack_array = np.sum([output_list_of_string[i][0:view_dict["M"]] for i in range(len(output_list_of_string))],axis=0,dtype=int)
            number_of_runs = np.sum([output_list_of_string[i][-2] for i in range(len(output_list_of_string))],axis=0,dtype=int)
            T = int(output_list_of_string[i][-1])
            file.close()
        except:
            pass

        input_dict_merged = dict(zip(list(input_dict.keys()),list(input_dict.values())))
        input_dict_merged["T"] = T
        input_dict_merged["number_of_runs"] = number_of_runs
        input_dict_merged["M"] = view_dict["M"]
        for m in range(len(stack_array)):
            input_dict_merged[m] = int(stack_array[m])

        data.append(input_dict_merged)

df = pd.DataFrame.from_records(data)
df.loc[-1] = df.dtypes
df.sort_index(inplace=True)

df[["alg_name","K","n","error_bool","meas_error_bool","error_rate","number_of_runs","T"]+[m for m in range(len(stack_array))]]

df.to_csv(path_data+"data_from_out.csv",index=False)