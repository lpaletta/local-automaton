import os
import sys
import time

import numpy as np
from multiprocessing import Pool, cpu_count, freeze_support

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

path_output = "repetition/measurement/out/"

from sgn import SIGNAL

import param as pm

number_of_cores = 8

def main():
    T_inner_job = pm.mc_dict["T_inner_job"]
    T_cum_max = pm.mc_dict["T_cum_max"]
    positive_max = pm.mc_dict["positive_max"]

    pm.param_dict.update(pm.param_sgn_dict)
    pm.option_dict.update(pm.option_sgn_dict)

    for i in range(len(pm.error_rate_list)):
        pm.param_dict["error_rate"] = pm.error_rate_list[i]
        for j in range(len(pm.meas_error_rate_list)):
            pm.param_dict["meas_error_rate"] = pm.meas_error_rate_list[j]
            for k in range(len(pm.K_list)):
                time_i = time.time()
                pm.param_dict["K"] = pm.K_list[k]

                print("Procede to: \n alg={}, K={}, e_d={}, e_m={}".format(pm.mc_dict["alg_name"],pm.param_dict["K"],pm.param_dict["error_rate"],pm.param_dict["meas_error_rate"]))

                param_dict,option_dict,view_dict,mc_dict = calibrate_param(pm.param_dict,pm.option_dict,pm.view_dict,pm.mc_dict)
                args = number_of_cores*[(param_dict,option_dict,view_dict,mc_dict)]

                T_cum=0
                positive=0
                positive_cum=0
                number_of_runs=0
                number_of_jobs=0

                while positive_cum<positive_max and T_cum<T_cum_max:
                    with Pool(number_of_cores) as pool:
                        results = pool.starmap(sMC, args)

                    result_positive = [r[0] for r in results]
                    result_number_of_runs = [r[1] for r in results]

                    positive+=np.sum(result_positive)
                    positive_cum+=np.sum(result_positive)
                    number_of_runs+=np.sum(result_number_of_runs)
                    number_of_jobs+=len(result_positive)

                    T_cum+=len(result_positive)*T_inner_job

                    if (np.sum(result_positive)>0) or ((T_inner_job*number_of_jobs)>=(T_cum_max/100)):
                        file = open(path_output+"data_{}_{}_{}.txt".format(i,j,k), "a")
                        file.write(str(positive)+" "+str(number_of_runs)+" "+str(param_dict["T"])+"\n")
                        file.close()
                        positive=0
                        number_of_runs=0
                        number_of_jobs=0
                
                time_f = time.time()
                print("Completed in: \n {}s".format(np.around(time_f-time_i,2)))

def calibrate_param(param,option,view,mc):
    for T_candidate in [10,20,50,100,200,500,1000]:
        positive=0
        number_of_param_jobs=0

        param["T"] = T_candidate
        args = number_of_cores*[(param,option,view,mc)]

        while number_of_param_jobs<100:
            with Pool(number_of_cores) as pool:
                results = pool.starmap(sMC, args)

            result_positive = [r[0] for r in results]
            result_number_of_param_jobs = [r[1] for r in results]

            positive+=np.sum(result_positive)
            number_of_param_jobs+=np.sum(result_number_of_param_jobs)
        
        if (positive/number_of_param_jobs)>0.1:
            param["T"] = T_candidate
            return(param,option,view,mc)
        
    param["T"] = 1000
    return(param,option,view,mc)

def sMC(param,option,view,mc):
    T_inner_job = mc["T_inner_job"]
    T = param["T"]
    positive = 0
    for i in range(T_inner_job//T):
        if mc["alg_name"] == "Signal":
            positive += SIGNAL(param, option, view)
    return(positive,T_inner_job//T)

def get_estimate_logical_signal(n,p,A,pth,gamma):
    pL = A*n*(p/pth)**gamma
    return(pL)

if __name__=="__main__":
    freeze_support()
    main()