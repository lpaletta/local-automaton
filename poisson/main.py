import sys

sys.path.append("/Users/lpaletta/Documents/INRIA/PhD/Cellular Automaton/Simulations/git")

from import_data import *
from plot import *

path, data_name = "git/poisson/data/", "data.csv"
path_fig = "git/poisson/fig/"

df = import_data(path, data_name, "Poisson")

plot_poisson(df,path_fig)