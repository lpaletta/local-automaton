import os
import sys
import time

import numpy as np
from multiprocessing import Pool, cpu_count, freeze_support

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

path_output = "git/stack/out/"

from sgn import SIGNAL
import param as pm

number_of_cores = 8

def main():
    T = pm.param_dict["T"]
    M = pm.view_dict["M"]
    T_cum_max = pm.mc_dict["T_cum_max"]
    positive_max = pm.mc_dict["positive_max"]
    
    pm.param_dict.update(pm.param_sgn_dict)
    pm.option_dict.update(pm.option_sgn_dict)
    
    for i in range(len(pm.error_rate_list)):
        pm.param_dict["error_rate"] = pm.error_rate_list[i]
        for j in range(len(pm.K_list)):
            time_i = time.time()
            pm.param_dict["K"] = pm.K_list[j]

            print("Procede to: \n alg={}, K={}, e={}".format(pm.mc_dict["alg_name"],pm.param_dict["K"],pm.param_dict["error_rate"]))

            args = number_of_cores*[(pm.param_dict,pm.option_dict,pm.view_dict)]

            T_cum=0
            positive_cum=0
            number_of_runs=0
            result_stack = np.zeros(M, dtype=np.int8)

            while positive_cum<positive_max and T_cum<T_cum_max:
                with Pool(number_of_cores) as pool:
                    results = pool.starmap(SIGNAL, args)

                result_stack = result_stack + sum([r for r in results])
                number_of_runs += len(results)
                T_cum=number_of_runs*T
                T_cum_temp=number_of_runs*T

                if T_cum_temp>=T_cum_max/100:
                    output = list(result_stack.astype(np.int32)) + [number_of_runs,T]
                    file = open(path_output+"data_{}_{}.txt".format(i,j), "a")
                    file.write(' '.join(map(str, output))+"\n")
                    file.close()
                    result_stack = np.zeros(M)
                    number_of_runs=0
                    T_cum_temp=0
            
            time_f = time.time()
            print("Completed in: \n {}s".format(np.around(time_f-time_i,2)))

if __name__=="__main__":
    freeze_support()
    main()