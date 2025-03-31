import numpy as np

def get_charge(syndrome_array,forward_signal_array,backward_signal_array,anti_signal_array,stack_array):
    excitation_array = forward_signal_array[0,:]+backward_signal_array[0,:]-(anti_signal_array[0,:]+stack_array[0,:])
    if np.shape(syndrome_array)[0]==1:
        syndrome_idx_array = np.nonzero(syndrome_array[0,:])[0]
        if syndrome_idx_array.size!=0:
            Q_array = np.zeros_like(syndrome_idx_array).astype(np.int32)
            for i in range(len(syndrome_idx_array)-1):
                Q_array[i] = np.sum(excitation_array[syndrome_idx_array[i]:syndrome_idx_array[i+1]])
                Q_array[-1] = np.sum(excitation_array[syndrome_idx_array[-1]:])+np.sum(excitation_array[:syndrome_idx_array[0]])
        elif syndrome_idx_array.size==0:
            Q_array = np.zeros(1).astype(np.int32)
            Q_array[0] = np.sum(excitation_array)
    if np.shape(syndrome_array)[0]==2:
        Q_array = np.zeros(1).astype(np.int32)
        Q_array[0] = np.sum(excitation_array)
    return(Q_array)

def get_charge_integral(syndrome_array,forward_signal_array,backward_signal_array,anti_signal_array,stack_array):
    syndrome_idx_array = np.nonzero(syndrome_array[0,:])[0]
    excitation_array = forward_signal_array[0,:]+backward_signal_array[0,:]-(anti_signal_array[0,:]+stack_array[0,:])
    if syndrome_idx_array.size!=0:
        i_charge_array = np.cumsum(np.roll(excitation_array,-syndrome_idx_array[0]))
    elif syndrome_idx_array.size==0:
        return(np.array([]))
    return(i_charge_array)

def update_global_hist(data_array,syndrome_array,forward_signal_array,backward_signal_array,anti_signal_array,stack_array,global_hist_array):
    global_array = np.vstack((data_array[0,:],syndrome_array[0,:],forward_signal_array[0,:],backward_signal_array[0,:],anti_signal_array[0,:],stack_array[0,:]))
    global_hist_array = np.concatenate((global_hist_array,global_array[:,np.newaxis,:]),axis=1)
    return(global_hist_array.astype(np.int8))