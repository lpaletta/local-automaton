import os
import sys

sys.path.append("/Users/lpaletta/Documents/INRIA/PhD/Cellular Automaton/Simulations/git")

from import_data import *
from analysis import *
from plot import *

path, data_name = "git/stack/data/", "data.csv"
path_fig = "git/stack/fig/"

df = import_data(path, data_name, "Stack")
df = get_integral(df)

######### plot pL #########

plot_distribution(df,path_fig,"stack_f_n.pdf")
for error_rate in list(set(df["error_rate"].to_list())):
    df_e = df[df["error_rate"]==error_rate]
    plot_distribution(df_e,path_fig,"stack_f_n_e={}.pdf".format(error_rate))