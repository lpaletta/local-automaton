import sys
import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, to_rgb

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from param import *

path_data = 'git/trajectory/data/'
path_fig = 'git/trajectory/fig/'

color_darkblue = to_rgb("#2E3192")
color_blue = to_rgb("#0071BC")
color_orange = to_rgb("#FBB03B")
color_gray = to_rgb("#E6E6E6")
color_green = to_rgb("#B6CBA0")
color_light_blue = to_rgb("#B4C8E6")
color_light_orange = to_rgb("#FAC88C")
linewidth = 1.5



with open(path_data+'global_hist_spacetime.npy', 'rb') as f:
    global_hist_array = np.load(f)

global_hist_array = global_hist_array[:,1:300,:]

data_hist_array = global_hist_array[0,:,:]

fig, ax = plt.subplots(figsize=(1,1))

ax.imshow(data_hist_array, cmap='Greys',  interpolation='none')
for spine in ax.spines.values():
    spine.set_linewidth(linewidth)
ax.spines['top'].set_linewidth(linewidth/3)    # Hide the top axis
ax.spines['bottom'].set_linewidth(linewidth/3) # Hide the bottom axis  # Hide the bottom axis
ax.spines['top'].set_color(color_gray)
ax.spines['bottom'].set_color(color_gray)
ax.spines['top'].set_zorder(-1)
ax.spines['bottom'].set_zorder(-1)

plt.tick_params(axis='both',which='both',bottom=False,left=False,labelbottom=False,labelleft=False)
fig.tight_layout(pad=0.1, w_pad=0.1, h_pad=0.1)
plt.savefig(path_fig+"/spacetime_data.pdf",)

syndrome_hist_array = global_hist_array[1,:,:]

fig, ax = plt.subplots(figsize=(1,1))

cmap = LinearSegmentedColormap.from_list("custom_cmap", [(1, 1, 1), color_blue])
ax.imshow(syndrome_hist_array, cmap=cmap,  interpolation='none')
for spine in ax.spines.values():
    spine.set_linewidth(linewidth)
ax.spines['top'].set_linewidth(linewidth/3)    # Hide the top axis
ax.spines['bottom'].set_linewidth(linewidth/3) # Hide the bottom axis  # Hide the bottom axis
ax.spines['top'].set_color(color_gray)
ax.spines['bottom'].set_color(color_gray)
ax.spines['top'].set_zorder(-1)
ax.spines['bottom'].set_zorder(-1)

plt.tick_params(axis='both',which='both',bottom=False,left=False,labelbottom=False,labelleft=False)
fig.tight_layout(pad=0.1, w_pad=0.1, h_pad=0.1)
plt.savefig(path_fig+"/spacetime_syndrome.pdf")

fig, ax = plt.subplots(figsize=(1,1))
syndrome_error_hist_array = syndrome_hist_array
syndrome_error_hist_array[0,:] = syndrome_hist_array[0,:] - (syndrome_hist_array[0,:]==0)*(data_hist_array[0,:]==1)

cmap = LinearSegmentedColormap.from_list("custom_cmap", [(1, 0, 0),(1, 1, 1), color_blue])
ax.imshow(syndrome_error_hist_array, cmap=cmap,  interpolation='none')
for spine in ax.spines.values():
    spine.set_linewidth(linewidth)
ax.spines['top'].set_linewidth(linewidth/3)    # Hide the top axis
ax.spines['bottom'].set_linewidth(linewidth/3) # Hide the bottom axis  # Hide the bottom axis
ax.spines['top'].set_color(color_gray)
ax.spines['bottom'].set_color(color_gray)
ax.spines['top'].set_zorder(-1)
ax.spines['bottom'].set_zorder(-1)

plt.tick_params(axis='both',which='both',bottom=False,left=False,labelbottom=False,labelleft=False)
fig.tight_layout(pad=0.1, w_pad=0.1, h_pad=0.1)
plt.savefig(path_fig+"/spacetime_syndrome_error.pdf")


forward_hist_array = global_hist_array[2,:,:]

fig, ax = plt.subplots(figsize=(1,1))

cmap = LinearSegmentedColormap.from_list("custom_cmap", [(1, 1, 1), color_light_blue])
ax.imshow(forward_hist_array, cmap=cmap,  interpolation='none')
for spine in ax.spines.values():
    spine.set_linewidth(linewidth)
ax.spines['top'].set_linewidth(linewidth/3)    # Hide the top axis
ax.spines['bottom'].set_linewidth(linewidth/3) # Hide the bottom axis  # Hide the bottom axis
ax.spines['top'].set_color(color_gray)
ax.spines['bottom'].set_color(color_gray)
ax.spines['top'].set_zorder(-1)
ax.spines['bottom'].set_zorder(-1)

plt.tick_params(axis='both',which='both',bottom=False,left=False,labelbottom=False,labelleft=False)
fig.tight_layout(pad=0.1, w_pad=0.1, h_pad=0.1)
plt.savefig(path_fig+"/spacetime_forward.pdf")

backward_hist_array = global_hist_array[3,:,:]

fig, ax = plt.subplots(figsize=(1,1))

cmap = LinearSegmentedColormap.from_list("custom_cmap", [(1, 1, 1), color_green])
ax.imshow(backward_hist_array, cmap=cmap,  interpolation='none')
for spine in ax.spines.values():
    spine.set_linewidth(linewidth)
ax.spines['top'].set_linewidth(linewidth/3)    # Hide the top axis
ax.spines['bottom'].set_linewidth(linewidth/3) # Hide the bottom axis
ax.spines['top'].set_color(color_gray)
ax.spines['bottom'].set_color(color_gray)
ax.spines['top'].set_zorder(-1)
ax.spines['bottom'].set_zorder(-1)

plt.tick_params(axis='both',which='both',bottom=False,left=False,labelbottom=False,labelleft=False)
fig.tight_layout(pad=0.1, w_pad=0.1, h_pad=0.1)
plt.savefig(path_fig+"/spacetime_backward.pdf")

anti_hist_array = global_hist_array[4,:,:]

fig, ax = plt.subplots(figsize=(1,1))

cmap = LinearSegmentedColormap.from_list("custom_cmap", [(1, 1, 1), color_light_orange])
ax.imshow(anti_hist_array, cmap=cmap, interpolation='none')
for spine in ax.spines.values():
    spine.set_linewidth(linewidth)
ax.spines['top'].set_linewidth(linewidth/3)    # Hide the top axis
ax.spines['bottom'].set_linewidth(linewidth/3) # Hide the bottom axis  # Hide the bottom axis
ax.spines['top'].set_color(color_gray)
ax.spines['bottom'].set_color(color_gray)
ax.spines['top'].set_zorder(-1)
ax.spines['bottom'].set_zorder(-1)

plt.tick_params(axis='both',which='both',bottom=False,left=False,labelbottom=False,labelleft=False)
fig.tight_layout(pad=0.1, w_pad=0.1, h_pad=0.1)
plt.savefig(path_fig+"/spacetime_anti.pdf")

stack_hist_array = global_hist_array[5,:,:]

fig, ax = plt.subplots(figsize=(1,1))

cmap = LinearSegmentedColormap.from_list("custom_cmap", [(1, 1, 1), color_orange])
ax.imshow(stack_hist_array, cmap=cmap,  interpolation='none')
for spine in ax.spines.values():
    spine.set_linewidth(linewidth)
ax.spines['top'].set_linewidth(linewidth/3)    # Hide the top axis
ax.spines['bottom'].set_linewidth(linewidth/3) # Hide the bottom axis  # Hide the bottom axis
ax.spines['top'].set_color(color_gray)
ax.spines['bottom'].set_color(color_gray)
ax.spines['top'].set_zorder(-1)
ax.spines['bottom'].set_zorder(-1)

plt.tick_params(axis='both',which='both',bottom=False,left=False,labelbottom=False,labelleft=False)
fig.tight_layout(pad=0.1, w_pad=0.1, h_pad=0.1)
plt.savefig(path_fig+"/spacetime_stack.pdf")

