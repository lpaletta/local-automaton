import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import matplotlib as mpl
import numpy as np

# use custom style
plt.style.use('rgplot')

khi_dict = {"9":0.59,
            "15":0.72,
            "25":0.67}

def plot_error_2D(df,n,fit_bool,bar_bool,path_fig):

    fig, ax = plt.subplots(1,1,figsize=(1.5,1.5))

    df_n = df[df["n"]==n]
    khi = list(df_n["khi"])[0]

    if not fit_bool:
        df_plot = df_n.pivot(index="meas_error_rate",columns="error_rate",values="pL")
    elif fit_bool:
        df_plot = df_n.pivot(index="meas_error_rate",columns="error_rate",values="pL_fit")

    x = np.array(df_plot.columns)
    y = np.array(df_plot.index)

    X, Y = np.meshgrid(x,y)
    Z = np.array(df_plot)
    
    pc = ax.pcolormesh(X,Y,Z,norm=LogNorm(vmin=10**(-9),vmax=10**(-3)),cmap='coolwarm')

    if bar_bool:
        cb = fig.colorbar(pc,ax=ax,orientation="horizontal",pad=0.35)
        cb.outline.set_linewidth(1.6)
        cb.set_ticks([10**(-9),10**(-6),10**(-3)])
        cb.ax.tick_params(labelsize=11,width=1.6)
        cb.ax.xaxis.set_label_position("top")
        cb.ax.xaxis.set_ticks_position("top")

    #ax.set_xlabel("$\\varepsilon_d$")
    #ax.set_ylabel("$\\varepsilon_m$")
    
        
    min_x, max_x = 0.005, 0.04
    plt.xlim(min_x, max_x)
    plt.ylim(min_x, max_x)

    if not fit_bool:
        C = 0.0225
        #khi = khi_dict[str(n)]
        X_level = np.linspace(0,1,100)
        Y_level = (1+1/khi)*C-1/khi*X_level
        ax.plot(X_level,Y_level,color='black',linewidth=1.3,linestyle='dotted')
        ax.text(0.4, 0.45, "$-m={}$".format(round(-1/khi,2)), color='black', fontsize=12, ha='center', va='center', transform=ax.transAxes,rotation=-360/(2*np.pi)*np.arctan(1/khi))

    ax.text(0.92, 0.87, "$n={}$".format(n), color='black', fontsize=12, ha='right', va='center', transform=ax.transAxes)

    ax.set_xticks([0.01,0.04])
    ax.set_yticks([0.01,0.02,0.03,0.04])
    ax.tick_params(axis='both', which='major', labelsize=11)
    ax.tick_params(axis='both', which='minor', labelsize=11)

    ax.grid(False)

    if not fit_bool:
        if bar_bool:
            fig.set_size_inches(2,2)
            fig.tight_layout(pad=1, w_pad=1, h_pad=1)
            plt.savefig(path_fig+"/analysis_measurement_error_wo_fit_n={}.pdf".format(n))
        else:
            ax.yaxis.set_label_position("right")
            ax.yaxis.tick_right()
            [i.set_linewidth(1.5) for i in ax.spines.values()]
            ax.xaxis.set_tick_params(width=1.6)
            ax.yaxis.set_tick_params(width=1.6)
            ax.set_aspect('equal')
            fig.tight_layout(pad=0.1, w_pad=0.1, h_pad=0.02)
            plt.savefig(path_fig+"/analysis_measurement_error_wo_fit_n={}_wo_bar.pdf".format(n))
    elif fit_bool:
        if bar_bool:
            fig.set_size_inches(2,2)
            fig.tight_layout(pad=1, w_pad=1, h_pad=1)
            plt.savefig(path_fig+"/analysis_measurement_error_fit_n={}.pdf".format(n))
        else:
            ax.yaxis.set_label_position("right")
            ax.yaxis.tick_right()
            [i.set_linewidth(1.6) for i in ax.spines.values()]
            ax.xaxis.set_tick_params(width=1.6)
            ax.yaxis.set_tick_params(width=1.6)
            ax.set_aspect('equal')
            fig.tight_layout(pad=0.05, w_pad=0.1, h_pad=0.01)
            plt.savefig(path_fig+"/analysis_measurement_error_fit_n={}_wo_bar.pdf".format(n))