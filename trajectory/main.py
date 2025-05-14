import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
from sgn import SIGNAL
from param import *
from utils import *

path_data = 'repetition/trajectory/data/'

K = 40
param_dict["K"] = 40

init_data_array = np.zeros((1,K)).astype(np.int8)

#Exemple
#init_data_array[0,0:3] = 1
#init_data_array[0,5:9] = 1
#init_data_array[0,11:13] = 1
#init_data_array[0,19:22] = 1
#init_data_array[0,24:28] = 1
#init_data_array[0,30:32] = 1

#param_sgn_dict["init_data_array"] = np.roll(init_data_array,2)

param_dict.update(param_sgn_dict)
option_dict.update(option_sgn_dict)

global_hist_array = SIGNAL(param_dict, option_dict, view_dict)

with open(path_data+'global_hist_spacetime.npy', 'wb') as f:
    np.save(f, global_hist_array)
