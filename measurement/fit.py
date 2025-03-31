import numpy as np

from scipy.optimize import curve_fit

# gamma and pth taken from logical
gamma_dict = {"9":4.7,
                  "15":7,
                  "25":9.5}

pth=0.065

def fit_eq_meas(df,n):

    df_fit = df.copy()
    df_fit = df_fit.dropna(subset="pL")

    df_fit_n = df_fit[df_fit["n"]==n]

    gamma = gamma_dict[str(n)]

    guess = np.array([1,0.5])
    fit = curve_fit(f=ansatz,xdata=(df_fit_n["error_rate"].to_numpy(),df_fit_n["meas_error_rate"].to_numpy(),gamma*np.ones_like(df_fit_n["error_rate"].to_numpy())),ydata=np.log(df_fit_n["pL"].to_numpy()),p0=guess,bounds=(0,[10,5]))
    param_opt_value = fit[0]
    A, khi = param_opt_value[0], param_opt_value[1]

    return(A,khi)

def add_pL_fit(df,n,key,A,khi):
    gamma = gamma_dict[str(n)]
    df.loc[df["n"]==n,key] = np.exp(ansatz((df.loc[:,"error_rate"],df.loc[:,"meas_error_rate"],gamma*np.ones_like(df["error_rate"].to_numpy())),A*np.ones_like(df["error_rate"].to_numpy()),khi*np.ones_like(df["error_rate"].to_numpy())))
    df.loc[df["n"]==n,"khi"] = khi
    return(df)

def ansatz(X,A,khi):
    p_d, p_m, gamma = X
    return(np.log((A*((p_d + khi*p_m)/pth)**gamma)))