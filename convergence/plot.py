import numpy as np

import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb

# use custom style
plt.style.use('rgplot')

grey = to_rgb("#D6D6D6")
light_grey = to_rgb("#F1F1F1")

from scipy.interpolate import make_interp_spline, BSpline

def plot_f_T(df,fit_bool,path_fig):

    plt.gca().set_prop_cycle(plt.rcParams['axes.prop_cycle'])
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    df_plot = df.copy()
    df_plot = df_plot.dropna(subset="pL")

    for name_e, group_e in df_plot.groupby("error_rate"):
        fig, ax = plt.subplots(1,1,figsize=(2.5,2))

        i=0

        for n, group_n in group_e.groupby("n"):

            group_n_subset = group_n[group_n["T"].isin([2,3]+[t for t in range(1,200,3)])]
            X = group_n_subset["T"].to_numpy()
            Y = group_n_subset["pL"].to_numpy()
            S = group_n_subset["sigma"].to_numpy()

            if n == 35:
                ax.errorbar(X,Y,yerr=S,capsize=1,markersize=2,fmt='o',color=grey,label="$n=%i$"%n)
            else:
                ax.errorbar(X,Y,yerr=S,capsize=1,markersize=2,fmt='o',color=colors[i],label="$n=%i$"%n)
                i+=1

            if fit_bool:
                Y = group_n_subset["pL_fit"].to_numpy()
                ax.plot(X,Y,linestyle="dotted",color=colors[i])

        ax.set_xlim(0,200)

        ax.set_yscale("log")
        ax.set_ylim(10**(-10),10**(-4))

        ax.set_xlabel("simulation time ($\\tau$)",fontsize=7,labelpad=0.5)
        ax.set_ylabel("normalized logical flip ($P_L(\\tau)/\\tau$)",fontsize=7,labelpad=0.5)

        ax.tick_params(axis='both', which='major', labelsize=7)
        ax.tick_params(axis='both', which='minor', labelsize=7)

        ax.grid(False)

        fig.tight_layout(pad=0.1,w_pad=0.1, h_pad=0.1)

        if fit_bool:
            plt.savefig(path_fig+"/logical_f_T_e={}.pdf".format(name_e))
        else:
            plt.savefig(path_fig+"/logical_f_T_e={}_wo_fit.pdf".format(name_e))
        plt.close()

def plot_transient_f_n(df,path_fig):

    fig, ax = plt.subplots(1,1,figsize=(1.5,2))

    df_plot = df.copy()
    df_plot = df_plot[["n","T_steady","T_steady_fit"]]
    df_plot = df_plot.drop_duplicates()

    X = df_plot["n"].to_numpy()
    Y = df_plot["T_steady"].to_numpy()

    ax.scatter(X,Y,s=10,color="black",facecolors='black',marker='D')

    X_fit = df_plot[df_plot["n"]>=10]["n"].to_numpy()
    Y_fit = df_plot[df_plot["n"]>=10]["T_steady_fit"].to_numpy()

    ax.plot(X_fit,Y_fit,color="black",linestyle="dotted",zorder=-1)

    ax.set_xlim(0,50)
    ax.set_ylim(0,100)

    ax.set_xlabel("number of qubits (n)",fontsize=7,labelpad=0.5)
    ax.set_ylabel("cut-off time ($\\tau_n$)",fontsize=7,labelpad=5,rotation=-90)

    ax.tick_params(axis='both', which='major', labelsize=7)
    ax.tick_params(axis='both', which='minor', labelsize=7)
    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()

    ax.grid(False)

    fig.tight_layout(pad=0.1, w_pad=0.1, h_pad=0.1)

    plt.savefig(path_fig+"/transient_f_n.pdf")
    plt.close()
