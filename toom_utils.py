import numpy as np

def error_channel(h,L,error_rate,rng):
    new_errors_array = (rng.random((h,L)) < error_rate)
    return(new_errors_array.astype(np.int8))

def get_syndrome(data_array,meas_error_bool,meas_error_rate,rng):
    h, L = np.shape(data_array)

    if meas_error_bool:
        syndrome_vert = (data_array != np.roll(data_array,-1,axis=0)) + error_channel(h,L,meas_error_rate,rng)
        syndrome_hor = (data_array != np.roll(data_array,-1,axis=1)) + error_channel(h,L,meas_error_rate,rng)
    else:
        syndrome_vert = (data_array != np.roll(data_array,-1,axis=0))
        syndrome_hor = (data_array != np.roll(data_array,-1,axis=1))
    
    return(syndrome_hor.astype(np.int8),syndrome_vert.astype(np.int8))

def get_correction_periodic(syndrome_hor,syndrome_vert):
    correction_array = syndrome_hor*syndrome_vert
    return(correction_array.astype(np.int8))

def get_correction_non_periodic(syndrome_hor,syndrome_vert,direction):

    correction_array_sw = syndrome_hor*np.roll(syndrome_vert,1,axis=0)
    correction_array_nw = syndrome_hor*syndrome_vert
    correction_array_se = np.roll(syndrome_hor,1,axis=1)*np.roll(syndrome_vert,1,axis=0)
    correction_array_ne = np.roll(syndrome_hor,1,axis=1)*syndrome_vert

    if direction == (1,1): #NW
        correction_array = correction_array_nw
        correction_array[-1,:], correction_array[:,-1], correction_array[-1,-1] = correction_array_sw[-1,:], correction_array_ne[:,-1], correction_array_se[-1,-1]

    if direction == (1,-1): #NE
        correction_array = correction_array_ne
        correction_array[-1,:], correction_array[:,0], correction_array[-1,0] = correction_array_se[-1,:], correction_array_nw[:,0], correction_array_sw[-1,0]  

    if direction == (-1,1): #SW
        correction_array = correction_array_sw
        correction_array[0,:], correction_array[:,-1], correction_array[0,-1] = correction_array_nw[0,:], correction_array_se[:,-1], correction_array_ne[0,-1]  

    if direction == (-1,-1): #SE
        correction_array = correction_array_se
        correction_array[0,:], correction_array[:,0], correction_array[0,0] = correction_array_ne[0,:], correction_array_sw[:,0], correction_array_nw[0,0] 
    
    return(correction_array.astype(np.int8))

def SWAP(data_array): #Equivalent to SWAP up to row permutation
    data_array[0,:] = np.roll(data_array[0,:],1)
    data_array[1,:] = np.roll(data_array[1,:],-1)
    return(data_array)