import numpy as np
import pandas as pd
pd.options.mode.chained_assignment = None

def import_data(path,data_name,analysis_var):
    dtypes = pd.read_csv(path+data_name, nrows=1, na_filter=False).iloc[0].to_dict()
    df = pd.read_csv(path+data_name,dtype=dtypes,skiprows=[1], na_filter=True)

    df["T"] = df["T"] + 1
    df['error_rate'] = df.apply(lambda x: np.around(x['error_rate'],4),axis=1)

    if analysis_var in ["Logical","Proof","Correlation","Measurement"]:
        if analysis_var != "Proof":
            df = df[df["positive"]>=10]
            df = df[df["number_of_runs"]>=2.5*df["positive"]]

        df['pL'] = df.apply(lambda x: compute_pL(positive=x['positive'],T=x['T'],number_of_runs=x['number_of_runs']),axis=1)
        df["sigma"] = df.apply(lambda x: compute_sigma(positive=x['positive'],T=x['T'],number_of_runs=x['number_of_runs']),axis=1)

    if analysis_var == "Measurement":
        df['meas_error_rate'] = df.apply(lambda x: np.around(x['meas_error_rate'],4),axis=1)

    elif analysis_var == "Poisson":
        df['ratio'] = df.apply(lambda x: compute_ratio(positive=x['positive'],number_of_runs=x['number_of_runs']),axis=1)
        df["sigma"] = df.apply(lambda x: compute_sigma_ratio(positive=x['positive'],number_of_runs=x['number_of_runs']),axis=1)

    elif analysis_var == "Stack":
        M = df["M"].iloc[0]

    if (analysis_var == "Logical") or (analysis_var == "Proof"):
        df = df.set_index(["alg_name","n","error_rate"]).unstack(fill_value=0).stack().reset_index()
        df[["pL","sigma"]] = df[["pL","sigma"]].replace(0, float("NaN"))
        df = df[["alg_name","n","T","error_rate","pL","sigma","positive","number_of_runs"]]

    elif analysis_var == "Correlation":
        df = df.set_index(["alg_name","n","error_rate","T"]).unstack(fill_value=0).stack().reset_index()
        df[["pL","sigma"]] = df[["pL","sigma"]].replace(0, float("NaN"))
        df = df[["alg_name","n","T","error_rate","pL","sigma","positive","number_of_runs"]]

    elif analysis_var == "Measurement":
        df = df.set_index(["alg_name","n","error_rate","meas_error_rate"]).unstack(fill_value=0).stack().reset_index()
        df[["pL","sigma"]] = df[["pL","sigma"]].replace(0, float("NaN"))
        df = df[["alg_name","n","T","error_rate","meas_error_rate","pL","sigma","positive","number_of_runs"]]

    elif analysis_var == "Poisson":
        df = df.set_index(["alg_name","n","error_rate","T"]).unstack(fill_value=0).stack().reset_index()
        df[["ratio","sigma"]] = df[["ratio","sigma"]].replace(0, float("NaN"))
        df["ratio"] = df["ratio"].fillna(1)
        df["sigma"] = df["sigma"].fillna(0)
        df = df[["alg_name","n","T","error_rate","ratio","sigma","positive","number_of_runs"]]

    elif analysis_var == "Stack":
        M = df["M"].iloc[0]
        df = df.set_index(["alg_name","n","error_rate","T"]).unstack(fill_value=0).stack().reset_index()
        df = df[["alg_name","n","T","error_rate","number_of_runs","M"]+[str(m) for m in range(M)]]

    return(df)

def compute_pL(positive,T,number_of_runs):
    r = positive/number_of_runs
    if r<=0.5:
        return((1-(1-2*r)**(1/T))/2)
    else:
        return(0.5)
    
def compute_ratio(positive,number_of_runs):
    r = positive/number_of_runs
    if r<0.5:
        return(r)
    elif r>0.5:
        return(0.5)
    
def compute_sigma(positive,T,number_of_runs):
    r = positive/number_of_runs
    return(1.96*np.sqrt(r*(1-r))/(T*np.sqrt(number_of_runs)))

def compute_sigma_ratio(positive,number_of_runs):
    r = positive/number_of_runs
    return(1.96*np.sqrt(r*(1-r))/(np.sqrt(number_of_runs)))