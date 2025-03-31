import sys
sys.path.append("/Users/lpaletta/Documents/INRIA/PhD/Cellular Automaton/Simulations/git")

from import_data import *
from fit import *
from plot import *

path, data_name = "git/measurement/data/", "data.csv"
path_fig = "git/measurement/fig/"

df = import_data(path, data_name, "Measurement")

for n in list(set(df["n"].to_list())):
    A, khi = fit_eq_meas(df,n)
    df = add_pL_fit(df,n,"pL_fit",A,khi)

for n in list(set(df["n"].to_list())):
    plot_error_2D(df,n,False,False,path_fig)
    plot_error_2D(df,n,False,True,path_fig)

for n in list(set(df["n"].to_list())):
    plot_error_2D(df,n,True,False,path_fig)

