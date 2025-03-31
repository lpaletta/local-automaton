import os
import sys

sys.path.append("/Users/lpaletta/Documents/INRIA/PhD/Cellular Automaton/Simulations/git")

from import_data import *
from analysis import *
from plot import *

path, data_name = "git/correlation/data/", "data.csv"
path_fig = "git/correlation/fig/"

df = import_data(path, data_name, "Correlation")
df = get_end_transient(df)
A, B = fit_end_transient(df[df["n"]>=10])
df = add_fit_transient(df,A,B)

plot_f_T(df,False,path_fig)
plot_transient_f_n(df,path_fig)











