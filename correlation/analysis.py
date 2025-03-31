import numpy as np
from scipy.stats import linregress

def get_end_transient(df):

    for name, group in df.groupby("n"):
        pL_mean = group[group["T"]>=100]["pL"].mean()
        group_steady = group[group["pL"]>=pL_mean/2]
        T_steady = group_steady["T"].min()

        df.loc[(df["n"]==name),"pL_mean"] = pL_mean
        df.loc[(df["n"]==name),"T_steady"] = T_steady

    return(df)

def fit_end_transient(df):

    df_temp = df[df["T"] == np.max(df["T"])]
    X = df_temp["n"].to_numpy()
    Y = df_temp["T_steady"].to_numpy()
    res = linregress(X,Y)
    return(res.slope, res.intercept)

def add_fit_transient(df,A,B):
    df["T_steady_fit"] = A*df["n"]+B
    return(df)
    