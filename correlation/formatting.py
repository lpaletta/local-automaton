import pandas as pd
from param import *

data = []

path_out = "git/correlation/out/"
path_data = "git/correlation/data/"

param_dict.update(param_sgn_dict)
option_dict.update(option_sgn_dict)
input_dict = param_dict | option_dict | mc_dict

for i in range(len(error_rate_list)):
    input_dict["error_rate"] = error_rate_list[i]
    for j in range(len(K_list)):
        input_dict["K"] = K_list[j]
        input_dict["n"] = input_dict["K"]

        positive_array = np.zeros(len([t for t in range(0,param_dict["T"],view_dict["dt"])]))
        number_of_runs = 0

        try:
            file = open(path_out+'data_'+str(i)+'_'+str(j)+'.txt')
            output_list_of_string = [s.split(" ") for s in file.readlines()]

            positive_array_k = np.array([float(output_list_of_string[i][0]) for i in range(len(output_list_of_string))])
            number_of_runs_k = np.array([float(output_list_of_string[i][1]) for i in range(len(output_list_of_string))])
            T_array_k = np.array([float(output_list_of_string[i][2]) for i in range(len(output_list_of_string))])

            data_k = {"positive":positive_array_k,
            "number_of_runs":number_of_runs_k,
            "T":T_array_k}

            df_k = pd.DataFrame(data_k)
            df_k_stacked = df_k.groupby('T').sum().reset_index()

            T_array = np.array(df_k_stacked["T"])
            positive_array = positive_array + np.array(df_k_stacked["positive"])
            number_of_runs = number_of_runs + np.array(df_k_stacked["number_of_runs"])
            
            file.close()
        except:
            pass

        try:
            for t in range(len(T_array)):
                
                input_dict_merged = dict(zip(list(input_dict.keys()),list(input_dict.values())))
                input_dict_merged["T"] = int(T_array[t])
                input_dict_merged["number_of_runs"] = int(number_of_runs[t])
                input_dict_merged["positive"] = int(positive_array[t])
                data.append(input_dict_merged)
        except:
            pass

df = pd.DataFrame.from_records(data)
df.loc[-1] = df.dtypes
df.sort_index(inplace=True)

df = df[["alg_name","K","n","error_bool","meas_error_bool","error_rate","positive","number_of_runs","T"]]

df.to_csv(path_data+"data_from_out.csv",index=False)