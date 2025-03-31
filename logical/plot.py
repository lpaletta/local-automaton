import numpy as np

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.colors import to_rgb
import matplotlib.patches as patches

grey = to_rgb("#D6D6D6")
light_grey = to_rgb("#F1F1F1")

def plot_f_n(df,fit_bool,key,plim_fit,path_fig):
    fig, ax = plt.subplots(1,1,figsize=(4,3))
    df_plot = df.copy()

    M=len(set(df_plot["error_rate"]))
    color_list = [plt.get_cmap('viridis')(i/M) for i in range(M)]
    i=0

    for name, group in df_plot.groupby("error_rate"):
        X = group["n"].to_numpy()
        Y = group["pL"].to_numpy()
        S = group["sigma"].to_numpy()
        ax.errorbar(X,Y,yerr=S,fmt="o",color=color_list[i],capsize=2.5,markersize=5,label="$\\epsilon=%.3f$"%name)
        i+=1

    if fit_bool:
        i=0
        for name, group in df_plot.groupby("error_rate"):
            group = group[group["error_rate"]<plim_fit]
            ax.plot(group["n"].to_numpy(), group[key].to_numpy(),color=color_list[i], linestyle='dotted')
            i+=1
        pth = df_plot["pth"].iloc[0]
        ax.set_title("$\\epsilon_L = An(\\epsilon/\\epsilon_{th})^{\\gamma_n}: \\epsilon_{th}=%.3f$"%(pth))
        
    ax.set_xlabel("$n$")
    ax.set_xlim(0,105)

    ax.set_ylabel("$\\epsilon_L$")
    ax.set_yscale("log")
    ax.set_ylim(10**(-9),10**(-1))

    ax.legend(loc="upper right")
    ax.legend(handletextpad=0.1)
    ax.legend(frameon=False)

    fig.tight_layout(pad=0.1, w_pad=0.1, h_pad=0.1)

    if not fit_bool:
        plt.savefig(path_fig+"/logical_f_n_wo_fit.pdf")
    elif fit_bool:
        plt.savefig(path_fig+"/logical_f_n_{}.pdf".format(key))
    plt.close()

def plot_f_E(df,fit_bool,key,plim_fit,path_fig):
    fig, ax = plt.subplots(1,1,figsize=(2.7,2.4))
    df_plot = df.copy()
    df_plot = df_plot.reset_index()

    M=len(set(df_plot["n"]))
    color_map = plt.get_cmap('tab10')
    i=0

    for name, group in df_plot.groupby("n"):
        X = group["error_rate"].to_numpy()
        Y = group["pL"].to_numpy()
        S = group["sigma"].to_numpy()
        if name <= 6:
            ax.errorbar(X,Y,yerr=S,fmt="o",color=grey,capsize=2.5,markersize=5,label="$n=%i$"%name)
        elif name > 6:
            ax.errorbar(X,Y,yerr=S,fmt="o",color=color_map(i),capsize=2.5,markersize=5,label="$n=%i$"%name)
            i+=1

    if fit_bool:
        i=0
        for name, group in df_plot.groupby("n"):
            group = group[group["error_rate"]<plim_fit]
            if name <= 6:
                ax.plot(group["error_rate"].to_numpy(), group[key].to_numpy(),color=grey, linestyle='dotted')
            elif name > 6:
                ax.plot(group["error_rate"].to_numpy(), group[key].to_numpy(),color=color_map(i), linestyle='dotted')
                i+=1

        pth = df_plot["pth"].iloc[0]
        ax.set_title("$\\epsilon_L = An(\\epsilon/\\epsilon_{th})^{\\gamma_n}: \\epsilon_{th}=%.3f$"%(pth))

    ax.set_xlabel("physical error ($\\epsilon = \\epsilon_d = \\epsilon_m$)",fontsize=7,labelpad=0.5)
    ax.set_ylabel("logical error ($\\epsilon_L$)",fontsize=7,labelpad=0.5)

    ax.set_xscale("log")
    ax.set_xlim(10**(-3),0.072)

    ax.set_yscale("log")
    ax.set_ylim(10**(-9),10**(-1))

    ax.tick_params(axis='both', which='major', labelsize=6)
    ax.tick_params(axis='both', which='minor', labelsize=6)

    ax.legend(loc="upper left",frameon=False,handletextpad=0.1,labelspacing=0.25,borderpad=0.25,fontsize=7)
    
    fig.tight_layout(pad=0.1, w_pad=0.1, h_pad=0.1)

    if not fit_bool:
        plt.savefig(path_fig+"/logical_f_E_wo_fit.pdf")
    elif fit_bool:
        plt.savefig(path_fig+"/logical_f_E_{}.pdf".format(key))
    plt.close()

def plot_gamma_n(df,fit_bool,key,path_fig):

    fig, ax = plt.subplots(1,1,figsize=(1.9,2.4))

    for name_alg, group_alg in df.groupby('alg_name'):
        if name_alg in ["Signal","Toom","Shearing"]:
            if name_alg=="Signal":

                n_reduced_list = list(set(group_alg["n"].to_list()))
                group_alg = group_alg[group_alg["n"].isin(n_reduced_list)] 

                X = group_alg["n"].to_numpy()
                Y = group_alg["gamma_n"].to_numpy()
                #ax.plot(X,Y,color="tab:blue",linewidth=1)
                #ax.scatter(X,Y,facecolors='tab:blue', edgecolors='tab:blue',marker='o',s=10,linewidths=1,zorder=10)
                #ax.errorbar(X,Y,0,color='tab:blue',fmt="o",capsize=2.5,markersize=5,label="SSR")
                #ax.plot(X,Y,'o-',color='tab:blue',markersize=3.5,linewidth=1,zorder=2,label="SSR")
                ax.scatter(X,Y,facecolors='tab:blue', edgecolors='tab:blue',marker='o',s=14,linewidths=1,zorder=-10,label="SSR")
                ax.plot(X,Y,color="tab:blue",linewidth=1,zorder=-10)
            elif name_alg=="Toom":

                X = group_alg["n"].to_numpy()
                Y = group_alg["gamma_n"].to_numpy()
                #ax.plot(X,Y,color="black",linestyle="dotted",linewidth=1)
                #ax.scatter(X,Y,facecolors='black', edgecolors='black',marker='s',s=10,linewidths=1,zorder=10)
                #ax.errorbar(X,Y,0,color='black',fmt="s",capsize=2.5,markersize=5,label="Toom")
                ax.scatter(X,Y,facecolors='black', edgecolors='black',marker='s',s=10,linewidths=1,zorder=-26,label="Toom")
                ax.plot(X,Y,color="black",linewidth=1,zorder=-26)
                #ax.plot(X,Y,'s-',color='black',markersize=3,linewidth=1,zorder=-1,label="Toom")
            elif name_alg=="Shearing":

                X = group_alg["n"].to_numpy()
                Y = group_alg["gamma_n"].to_numpy()
                #ax.plot(X,Y,color="black",linestyle="dotted",linewidth=1)
                #ax.scatter(X,Y,facecolors='black', edgecolors='black',marker='^',s=15,linewidths=1,zorder=10)
                #ax.plot(X,Y,'^-',color='tab:green',markersize=3,linewidth=1,zorder=1,label="Shear.")
                ax.scatter(X,Y,facecolors='tab:green', edgecolors='tab:green',marker='^',s=18,linewidths=1,zorder=-15,label="Shear.")
                ax.plot(X,Y,color="tab:green",linewidth=1,zorder=-15)

    
            
    X = np.linspace(0,100,50)
    Y = (X+1)/2
    ax.plot(X,Y,color="black",linestyle="dashdot",zorder=-40,label=" $\\frac{n+1}{2}$")

    df  = df[df["n"]>15]

    if fit_bool:
        i=0
        for name_alg, group_alg in df.groupby("alg_name"):
            if name_alg in ["Signal","Toom"]:
                alpha = group_alg["alpha"].iloc[0]
                beta = group_alg["beta"].iloc[0]
                label="$\\alpha=%.2f, \\beta=%.2f$"%(alpha,beta)
                ax.plot(group_alg["n"].to_numpy(), group_alg[key].to_numpy(), linestyle='dashed',label=label)
                ax.set_title("$\\epsilon_L = An(\\epsilon/\\epsilon_{th})^{\\gamma_n}$")
            i+=1

    ax.set_xlabel("number of qubits ($n$)",labelpad=0.5,fontsize=7.5,)
    ax.set_xlim(0,100)

    ax.set_ylabel("effective distance ($\\gamma_n$)",labelpad=0.5,fontsize=7.5)
    ax.set_ylim(0,20)

    ax.tick_params(axis='both', which='major', labelsize=7)
    ax.tick_params(axis='both', which='minor', labelsize=7)

    try:
        handles, labels = plt.gca().get_legend_handles_labels()
        order=[1,0,2,3]
        ax.legend([handles[idx] for idx in order],[labels[idx] for idx in order],loc="lower right",frameon=False,fontsize=7)
    except:
        ax.legend(loc="lower right",frameon=False,fontsize=7)

    fig.tight_layout(pad=0.4, w_pad=0.1, h_pad=0.1)

    if not fit_bool:
        plt.savefig(path_fig+"/gamma_f_n_wo_fit.pdf")
    elif fit_bool:
        plt.savefig(path_fig+"/gamma_f_n.pdf")
    plt.close()

def plot_estimate_f_n(df,df_proof,path_fig):
    fig, ax = plt.subplots(1,1,figsize=(2.55,2.4))

    rect = patches.Rectangle((10**(-9), 0), 1, 100, linewidth=0, edgecolor=None, facecolor=light_grey,zorder=-40)
    ax.add_patch(rect)

    df_plot = df.copy()
    df_plot = df_plot.reset_index()

    for name, group in df_plot.groupby("alg_name"):
        if name=="Signal":
            error_rate=0.001
            group_0001=group[group["error_rate"]==error_rate]
            X_proof = df_proof[df_proof["error_rate"]==error_rate]["pL"].to_numpy()
            Y_proof = df_proof[df_proof["error_rate"]==error_rate]["n"].to_numpy()
            S_proof = df_proof[df_proof["error_rate"]==error_rate]["sigma"].to_numpy()
            ax.scatter(X_proof,Y_proof,facecolors='white', edgecolors='tab:blue',marker='o',s=50,linewidths=1,zorder=-8)
            ax.errorbar(X_proof,Y_proof,xerr=S_proof,fmt="o",color="tab:blue",capsize=3,markersize=6,zorder=-9)
            Y = group_0001["n"].to_numpy()
            X = group_0001["pL_fit"].to_numpy()
            Y_inf = group_0001[group_0001["pL_fit"]<10**(-9)]["n"].to_numpy()
            X_inf = group_0001[group_0001["pL_fit"]<10**(-9)]["pL_fit"].to_numpy()
            Y_sup = group_0001[group_0001["pL_fit"]>10**(-9)]["n"].to_numpy()
            X_sup = group_0001[group_0001["pL_fit"]>10**(-9)]["pL_fit"].to_numpy()
            ax.scatter(X_inf,Y_inf,facecolors='white', edgecolors='tab:blue',marker='o',s=16,linewidths=1,zorder=-9)
            ax.scatter(X_sup,Y_sup,facecolors=light_grey, edgecolors='tab:blue',marker='o',s=16,linewidths=1,zorder=-0)
            ax.plot(X,Y,color="tab:blue",linewidth=1,zorder=-10)
            error_rate=0.01
            group_001=group[group["error_rate"]==error_rate]
            X_proof = df_proof[df_proof["error_rate"]==error_rate]["pL"].to_numpy()
            Y_proof = df_proof[df_proof["error_rate"]==error_rate]["n"].to_numpy()
            S_proof = df_proof[df_proof["error_rate"]==error_rate]["sigma"].to_numpy()
            ax.errorbar(X_proof,Y_proof,xerr=S_proof,fmt="o",color="tab:blue",capsize=3,markersize=6,zorder=-9)
            Y = group_001["n"].to_numpy()
            X = group_001["pL_fit"].to_numpy()
            ax.scatter(X,Y,facecolors='tab:blue', edgecolors='tab:blue',marker='o',s=16,linewidths=1,zorder=-10)
            ax.plot(X,Y,color="tab:blue",linewidth=1,zorder=-10)
        elif name=="Toom":
            error_rate=0.001
            group_0001=group[group["error_rate"]==error_rate]
            Y = group_0001["n"].to_numpy()
            X = group_0001["pL_fit"].to_numpy()
            Y_inf = group_0001[group_0001["pL_fit"]<10**(-9)]["n"].to_numpy()
            X_inf = group_0001[group_0001["pL_fit"]<10**(-9)]["pL_fit"].to_numpy()
            Y_sup = group_0001[group_0001["pL_fit"]>10**(-9)]["n"].to_numpy()
            X_sup = group_0001[group_0001["pL_fit"]>10**(-9)]["pL_fit"].to_numpy()
            ax.scatter(X_inf,Y_inf,facecolors='white', edgecolors='black',marker='s',s=12,linewidths=1,zorder=-19)
            ax.scatter(X_sup,Y_sup,facecolors=light_grey, edgecolors='black',marker='s',s=12,linewidths=1,zorder=-19)
            ax.plot(X,Y,color="black",linewidth=1,zorder=-20)
            error_rate=0.01
            group_001=group[group["error_rate"]==error_rate]
            Y = group_001["n"].to_numpy()
            X = group_001["pL_fit"].to_numpy()
            ax.plot(X,Y,color="black",linewidth=1,zorder=-26)
            ax.scatter(X,Y,facecolors='black', edgecolors='black',marker='s',s=12,linewidths=1,zorder=-19)
        elif name=="Shearing":
            error_rate=0.001
            group_0001=group[group["error_rate"]==error_rate]
            Y = group_0001["n"].to_numpy()
            X = group_0001["pL_fit"].to_numpy()
            Y_inf = group_0001[group_0001["pL_fit"]<10**(-9)]["n"].to_numpy()
            X_inf = group_0001[group_0001["pL_fit"]<10**(-9)]["pL_fit"].to_numpy()
            Y_sup = group_0001[group_0001["pL_fit"]>10**(-9)]["n"].to_numpy()
            X_sup = group_0001[group_0001["pL_fit"]>10**(-9)]["pL_fit"].to_numpy()
            ax.plot(X,Y,color="tab:green",linewidth=1,zorder=-15)
            ax.scatter(X_inf,Y_inf,facecolors='white', edgecolors='tab:green',marker='^',s=22,linewidths=1,zorder=-14)
            ax.scatter(X_sup,Y_sup,facecolors=light_grey, edgecolors='tab:green',marker='^',s=22,linewidths=1,zorder=-14)
            error_rate=0.01
            group_001=group[group["error_rate"]==error_rate]
            Y = group_001["n"].to_numpy()
            X = group_001["pL_fit"].to_numpy()
            ax.plot(X,Y,color="tab:green",linewidth=1,zorder=-15)
            ax.scatter(X,Y,facecolors='tab:green', edgecolors='tab:green',marker='^',s=22,linewidths=1,zorder=16)

    ax.scatter([],[],color=light_grey,linewidth=1,label="$\\varepsilon = 10^{-2}$")
    ax.scatter([],[],color=light_grey,linewidth=1,label="$\\varepsilon = 10^{-3}$")

    ax.set_xlabel("logical error ($\\epsilon_L$)",fontsize=7.5,labelpad=0.5)
    ax.set_ylabel("number of qubits ($n$)",fontsize=7.5,labelpad=5,rotation=-90)

    ax.set_xscale("log")
    ax.set_xlim(10**(-14),10**(-6))
    ax.set_ylim(0,100)

    ax.tick_params(axis='both', which='major', labelsize=7)
    ax.tick_params(axis='both', which='minor', labelsize=7)

    ax.yaxis.set_label_position("right")
    ax.yaxis.tick_right()

    ax.legend(loc="upper right",fontsize=7,frameon=False)

    fig.tight_layout(pad=0.1, w_pad=0.1, h_pad=0.1)

    plt.savefig(path_fig+"/logical_estimate_f_n.pdf")
    
    plt.close()