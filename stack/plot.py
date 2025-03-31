import numpy as np
import matplotlib.pyplot as plt
from import_data import *

def compute_sigma(stack_value, T, number_of_runs):
    if stack_value.all() == 0:
        return(0)
    else:
        r = stack_value / number_of_runs
        return 1.96 * np.sqrt(r * (1 - r)) / (T * np.sqrt(number_of_runs))

def plot_distribution(df,path_fig,name):

    fig, ax = plt.subplots(1,1,figsize=(4.5,2.2))

    ax.scatter([],[],color='black',s=40,label="$\\varepsilon = 10^{-2}$")
    ax.scatter([],[],edgecolors='black',facecolors="white",s=40,label="$\\varepsilon = 10^{-3}$")

    for error_rate in list(set(df["error_rate"].to_list())):
        df_e = df[df["error_rate"]==error_rate]
        plt.gca().set_prop_cycle(plt.rcParams['axes.prop_cycle'])

        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
        i = 0

        for n, group in df_e.groupby("n"):
            color = colors[i]

            M = int(group["M"].iloc[0])
            T = int(group["T"].iloc[0])
            number_of_runs = int(group["number_of_runs"].iloc[0])
            m_list = [str(m) for m in range(M)]

            X = np.array([int(m) for m in range(M)])
            Y = group[m_list].to_numpy()[0]
            number_of_entries = Y[0]
            Y = np.where(Y<10,0,Y)
            Y_norm = Y/(number_of_entries)
            S = compute_sigma(Y,T,number_of_runs)
            if error_rate == 0.01:
                ax.scatter(X,Y_norm,color=color,s=40,label="$n=%i$"%n)
                #ax.errorbar(X,Y_norm,S,fmt="D",capsize=2.2,markersize=4.4,label="$n=%i$"%n)
                #ax.step(X,Y_norm,where="post",label="$n=%i$"%n)
                #ax.errorbar(X,Y_norm,S,fmt="o",color=step[0].get_color(),capsize=1,markersize=2)
            elif error_rate == 0.001:
                ax.scatter(X,Y_norm,edgecolors=color,facecolors='white',s=40)
                #ax.errorbar(X,Y_norm,S,fmt="D",capsize=2.2,markersize=4.4)
                #ax.errorbar(X,Y_norm,0,fmt="D",color="white",capsize=1.4,markersize=2.8)
                #ax.step(X,Y_norm,where="post",linestyle="--")
            i += 1
    #ax.plot([],[],label="$\\varepsilon = 10^{-3}$",color='black',linestyle="dashdot")
    #ax.set_title("$\\varepsilon = {}$".format(error_rate))
    ax.set_xlabel("maximum stack ($m$)",fontsize=7.5,labelpad=0.5)
    ax.set_ylabel("survival function $(S_M(m))$",fontsize=7.5,labelpad=0.5)

    ax.set_xlim(0,16)
    ax.set_ylim(10**(-8),10**(0))
    #plt.xticks(np.arange(-0, 18, step=2))
    ax.set_yscale("log")

    ax.tick_params(axis='both', which='major', labelsize=7)
    ax.tick_params(axis='both', which='minor', labelsize=7)

    ax.legend(loc="upper right",frameon=False,fontsize=7)

    #ax.set_axisbelow(True)
    #ax.grid(True,which="both",linewidth=0.3)

    fig.tight_layout(pad=0.1, w_pad=0.1, h_pad=0.1)

    plt.savefig(path_fig+"/"+name)
    plt.close()

def get_integral(df):

    M = int(df["M"].iloc[0])
    m_list = [str(m) for m in range(M)]

    df_numeric = df[m_list]
    df_without_num = df.drop(columns=m_list)
    #print(df_numeric)
    df_cumsum = df_numeric.copy()
    for i in range(len(df_numeric.columns)):
        df_cumsum.iloc[:, i] = df_numeric.iloc[:, i:].sum(axis=1)
    df_result = pd.concat([df_without_num, df_cumsum], axis=1)
    return(df_result)