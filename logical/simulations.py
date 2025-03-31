import os
import sys
import time

import numpy as np
from multiprocessing import Pool, cpu_count, freeze_support

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

path_output = "git/logical/out/"

from sgn import SIGNAL
from toom import TOOM
from shearing import SHEARING

import param

number_of_cores = 8

def main():
    T_inner_job = param.mc_dict["T_inner_job"]
    T_cum_max = param.mc_dict["T_cum_max"]
    positive_max = param.mc_dict["positive_max"]

    for i in range(len(param.alg_list)):

        param.mc_dict["alg_name"] = param.alg_list[i]

        if param.mc_dict["alg_name"] == "Signal":
            K_list = param.K_sgn_list
            param.param_dict.update(param.param_sgn_dict)
            param.option_dict.update(param.option_sgn_dict)
        elif param.mc_dict["alg_name"] == "Toom":
            K_list = param.K_toom_list
            param.param_dict.update(param.param_toom_dict)
            param.option_dict.update(param.option_toom_dict)
        elif param.mc_dict["alg_name"] == "Shearing":
            K_list = param.K_shearing_list
            param.param_dict.update(param.param_shearing_dict)
            param.option_dict.update(param.option_shearing_dict)

        for j in range(len(param.error_rate_list)):
            param.param_dict["error_rate"] = param.error_rate_list[j]
            for k in range(len(K_list)):
                time_i = time.time()
                param.param_dict["K"] = K_list[k]

                print("Procede to: \n alg={}, K={}, e={}".format(param.mc_dict["alg_name"],param.param_dict["K"],param.param_dict["error_rate"]))

                if param.mc_dict["alg_name"] == "Signal":
                    A, pth, alpha, beta = 0.002, 0.067, 1, 0.6
                    n, p = param.param_dict["K"], param.param_dict["error_rate"]
                    estimate_logical = get_estimate_logical_signal(n,p,A,pth,alpha*n**beta)
                    print("Estimated logical rate: \n {}".format(estimate_logical))
                    if estimate_logical < 10**(-7):
                        continue
                    else:
                        pass

                if param.mc_dict["alg_name"] == "Toom":
                    A, pth, alpha, beta = 0.0015, 0.074, 0.85, 0.62
                    n, p = param.param_dict["K"]**2, param.param_dict["error_rate"]
                    estimate_logical = get_estimate_logical_signal(n,p,A,pth,alpha*n**beta)
                    print("Estimated logical rate: \n {}".format(estimate_logical))
                    if estimate_logical < 10**(-7):
                        continue
                    else:
                        pass

                if param.mc_dict["alg_name"] == "Shearing":
                    A, pth = 0.008, 0.11
                    n, p = param.param_dict["K"], param.param_dict["error_rate"]
                    estimate_logical = get_estimate_logical_signal(n,p,A,pth,min(10,n**0.6))
                    print("Estimated logical rate: \n {}".format(estimate_logical))
                    if estimate_logical < 10**(-7):
                        continue
                    else:
                        pass

                param_dict,option_dict,view_dict,mc_dict = calibrate_param(param.param_dict,param.option_dict,param.view_dict,param.mc_dict)
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
                #results = [sMC(param,option,view,mc) for i in range(10)]
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
        elif mc["alg_name"] == "Toom":
            positive += TOOM(param, option, view)
        elif mc["alg_name"] == "Shearing":
            positive += SHEARING(param, option, view)
    return(positive,T_inner_job//T)

def get_estimate_logical_signal(n,p,A,pth,gamma):
    pL = A*n*(p/pth)**gamma
    return(pL)

if __name__=="__main__":
    freeze_support()
    main()