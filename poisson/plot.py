import matplotlib.pyplot as plt
import numpy as np

import matplotlib.ticker as ticker
from matplotlib.colors import to_rgb

grey = to_rgb("#D6D6D6")

def plot_poisson(df,path_fig):

    fig, ax = plt.subplots(1,1,figsize=(2.5,2))
    ax.scatter([],[],s=1,label=" ",color='w')

    for n, group_n in df.groupby("n"):

        if n == 9:
            T_list = np.sort(list(set(df["T"].to_list())))
            T_list_reduced = [T_list[i] for i in range(len(T_list)) if i%2==0]

            group_n = group_n[group_n["T"].isin(T_list_reduced)]
        if n == 15:
            T_list = np.sort(list(set(df["T"].to_list())))
            T_list_reduced = [T_list[i] for i in range(len(T_list)) if i%10==0]

            group_n = group_n[group_n["T"].isin(T_list_reduced)]
        elif n > 15:
            T_list = np.sort(list(set(df["T"].to_list())))
            T_list_reduced = [T_list[i] for i in range(len(T_list)) if i%20==0]

            group_n = group_n[group_n["T"].isin(T_list_reduced)]

        group_n = group_n[group_n["positive"]<(45*group_n["number_of_runs"]/100)]

        X = group_n["T"].to_numpy()
        Y = 1-2*group_n["ratio"].to_numpy()
        S = 2*group_n["sigma"].to_numpy()
        
        if n == 35:
            ax.errorbar(X,Y,yerr=S,fmt="o",color=grey,capsize=1,markersize=2,label="n={}".format(n))
        else:
            ax.errorbar(X,Y,yerr=S,fmt="o",capsize=1,markersize=2,label="n={}".format(n))

    ax.set_xlim([1,10**6])
    plt.xticks([1,100000,500000,1000000], 
           ['$1$','$10^5$','$5 \\times 10^5$','$10^6$'])
    minor_ticks_x = [1*10**5,2*10**5,3*10**5,4*10**5,5*10**5,6*10**5,7*10**5,8*10**5,9*10**5]
    plt.gca().set_xticks(minor_ticks_x, minor=True)

    ax.set_yscale("log")
    ax.set_ylim([0.1,1])

    ax.tick_params(axis='both', which='major', labelsize=7)
    ax.tick_params(axis='both', which='minor', labelsize=7)
    ax.yaxis.set_minor_formatter(ticker.NullFormatter())

    ax.set_xlabel("simulation time ($\\tau$)",fontsize=7,labelpad=0.5)
    ax.set_ylabel("pop. in maj. 0 ($1-2 \\times P_L(\\tau)$)",fontsize=7,labelpad=0.5)

    ax.legend(loc="lower right",frameon=False,handletextpad=0.1,labelspacing=0.25,borderpad=0.25,fontsize=7,ncol=3,columnspacing=0.5)

    fig.tight_layout(pad=0.1, w_pad=0.1, h_pad=0.1)
    
    plt.savefig(path_fig+"/analysis_poisson.pdf")