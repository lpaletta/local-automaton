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

def SN(data_array,boundary_var,S):

    L, h = data_array.shape

    if L%2==0 and h%2==0:
        if S%4==0:
            for i in np.arange(0,L,1):
                for j in np.arange(0,h,2):
                    perm_hor(data_array,boundary_var,i,j)
        elif S%4==1:
            for i in np.arange(0,L,2):
                for j in np.arange(0,h,1):
                    perm_vert(data_array,boundary_var,i,j)
        elif S%4==2:
            for i in np.arange(0,L,1):
                for j in np.arange(1,h+1,2):
                    perm_hor(data_array,boundary_var,i,j)
        elif S%4==3:
            for i in np.arange(1,L+1,2):
                for j in np.arange(0,h,1):
                    perm_vert(data_array,boundary_var,i,j)

    elif L%2==1 and h%2==1:
        if S%4==0:
            for i in np.arange(0,L,1):
                for j in np.arange(0,h-1,2):
                    perm_hor(data_array,boundary_var,i,j)
        elif S%4==1:
            for i in np.arange(0,L-1,2):
                for j in np.arange(0,h,1):
                    perm_vert(data_array,boundary_var,i,j)
        elif S%4==2:
            for i in np.arange(0,L,1):
                for j in np.arange(1,h,2):
                    perm_hor(data_array,boundary_var,i,j)
        elif S%4==3:
            for i in np.arange(1,L,2):
                for j in np.arange(0,h,1):
                    perm_vert(data_array,boundary_var,i,j)

    return(data_array)

def SNA(data_array,boundary_var,S):

    L, h = data_array.shape

    if L%4==0:
        if S%4==0:
            for i in np.arange(0,L,2):
                for j in np.arange(0,L,2):
                    if (i+j)%4==0:
                        perm_hor(data_array,boundary_var,i,j)
                        perm_hor(data_array,boundary_var,i+1,j)
                    elif (i+j)%4==2:
                        perm_vert(data_array,boundary_var,i,j)
                        perm_vert(data_array,boundary_var,i,j+1)
        if S%4==1:
            for i in np.arange(0,L,2):
                for j in np.arange(0,L,2):
                    if (i+j)%4==0:
                        perm_vert(data_array,boundary_var,i,j)
                        perm_vert(data_array,boundary_var,i,j+1)
                    elif (i+j)%4==2:
                        perm_hor(data_array,boundary_var,i,j)
                        perm_hor(data_array,boundary_var,i+1,j)
        if S%4==2:
            for i in np.arange(1,L+1,2): #vertical
                if (i-1)%4==2:
                    perm_hor(data_array,boundary_var,i,-1)
                    perm_hor(data_array,boundary_var,i+1,-1)
                elif (i-1)%4==0:
                    perm_vert(data_array,boundary_var,i,0)
            for j in np.arange(1,L+1,2): #horizontal
                if (j-1)%4==2:
                    perm_hor(data_array,boundary_var,0,j)
                elif (j-1)%4==0:
                    perm_vert(data_array,boundary_var,-1,j)
                    perm_vert(data_array,boundary_var,-1,j+1)
            for i in np.arange(1,L-1,2):
                for j in np.arange(1,L-1,2):
                    if ((i-1)+(j-1))%4==0:
                        perm_hor(data_array,boundary_var,i,j)
                        perm_hor(data_array,boundary_var,i+1,j)
                    elif ((i-1)+(j-1))%4==2:
                        perm_vert(data_array,boundary_var,i,j)
                        perm_vert(data_array,boundary_var,i,j+1)
        if S%4==3:
            for i in np.arange(1,L+1,2): #vertical
                if (i-1)%4==0:
                    perm_hor(data_array,boundary_var,i,-1)
                    perm_hor(data_array,boundary_var,i+1,-1)
                elif (i-1)%4==2:
                    perm_vert(data_array,boundary_var,i,0)
            for j in np.arange(1,L+1,2): #horizontal
                if (j-1)%4==0:
                    perm_hor(data_array,boundary_var,0,j)
                elif (j-1)%4==2:
                    perm_vert(data_array,boundary_var,-1,j)
                    perm_vert(data_array,boundary_var,-1,j+1)
            for i in np.arange(1,L-1,2):
                for j in np.arange(1,L-1,2):
                    if ((i-1)+(j-1))%4==2:
                        perm_hor(data_array,boundary_var,i,j)
                        perm_hor(data_array,boundary_var,i+1,j)
                    elif ((i-1)+(j-1))%4==0:
                        perm_vert(data_array,boundary_var,i,j)
                        perm_vert(data_array,boundary_var,i,j+1)

    elif L%4>=1:
        if S%4==0:
            for i in np.arange(0,L,2):
                for j in np.arange(0,L,2):
                    if (i+j)%4==0:
                        perm_hor(data_array,"None",i,j)
                        perm_hor(data_array,"None",i+1,j)
                    if (i+j)%4==2:
                        perm_vert(data_array,"None",i,j)
                        perm_vert(data_array,"None",i,j+1)
        elif S%4==1:
            for i in np.arange(0,L,2):
                for j in np.arange(0,L,2):
                    if (i+j)%4==0:
                        perm_vert(data_array,"None",i,j)
                        perm_vert(data_array,"None",i,j+1)
                    if (i+j)%4==2:
                        perm_hor(data_array,"None",i,j)
                        perm_hor(data_array,"None",i+1,j)
        elif S%4==2:
            for i in np.arange(-1,L+1,2):
                for j in np.arange(-1,L+1,2):
                    if ((i+1)+(j+1))%4==0:
                        perm_hor(data_array,"None",i,j)
                        perm_hor(data_array,"None",i+1,j)
                    if ((i+1)+(j+1))%4==2:
                        perm_vert(data_array,"None",i,j)
                        perm_vert(data_array,"None",i,j+1)
        elif S%4==3:
            for i in np.arange(-1,L+1,2):
                for j in np.arange(-1,L+1,2):
                    if ((i+1)+(j+1))%4==0:
                        perm_vert(data_array,"None",i,j)
                        perm_vert(data_array,"None",i,j+1)
                    if ((i+1)+(j+1))%4==2:
                        perm_hor(data_array,"None",i,j)
                        perm_hor(data_array,"None",i+1,j)
    return(data_array)

def SND(data_array,boundary_var,S):

    L, h = data_array.shape

    if L%2==0 and h%2==0:
        if S%4==0:
            for j in np.arange(0,h,1):
                for i in np.arange(1,L+1,2):
                    perm_diag_av(data_array,boundary_var,i,j)
        elif S%4==1:
            for j in np.arange(0,h,1):
                for i in np.arange(1,L+1,2):
                    perm_diag_ar(data_array,boundary_var,i,j)
        elif S%4==2:
            for i in np.arange(1,L+1,1):
                for j in np.arange(0,h,2):
                    perm_diag_av(data_array,boundary_var,i,j)
        elif S%4==3:
            for i in np.arange(1,L+1,1):
                for j in np.arange(1,h+1,2):
                    perm_diag_ar(data_array,boundary_var,i,j)
                    

    elif L%2==1 and h%2==1:
        if S%8==0:
            for j in np.arange(0,h,1):
                for i in np.arange(1,L,2):
                    perm_diag_av(data_array,boundary_var,i,j)
            for j in np.arange(0,h,2):
                perm_hor(data_array,boundary_var,L-1,j)
        elif S%8==1:
            for j in np.arange(0,h,1):
                for i in np.arange(1,L,2):
                    perm_diag_ar(data_array,boundary_var,i,j)
            for j in np.arange(0,h,2):
                perm_hor(data_array,boundary_var,L-1,j+1)
        elif S%8==2:
            for i in np.arange(0,L,1):
                for j in np.arange(0,h-1,2):
                    perm_diag_av(data_array,boundary_var,i,j)
            for i in np.arange(0,L,2):
                perm_vert(data_array,boundary_var,i,h-1)
        elif S%8==3:
            for i in np.arange(0,L,1):
                for j in np.arange(1,h,2):
                    perm_diag_ar(data_array,boundary_var,i,j)
            for i in np.arange(0,L,2):
                perm_vert(data_array,boundary_var,i+1,h-1)
        elif S%8==4:
            for j in np.arange(0,h,1):
                for i in np.arange(2,L+1,2):
                    perm_diag_av(data_array,boundary_var,i,j)
            for j in np.arange(0,h,2):
                perm_hor(data_array,boundary_var,0,j)
        elif S%8==5:
            for j in np.arange(0,h,1):
                for i in np.arange(2,L+1,2):
                    perm_diag_ar(data_array,boundary_var,i,j)
            for j in np.arange(0,h,2):
                perm_hor(data_array,boundary_var,0,j+1)
        elif S%8==6:
            for i in np.arange(0,L,1):
                for j in np.arange(1,h,2):
                    perm_diag_av(data_array,boundary_var,i,j)
            for i in np.arange(0,L,2):
                perm_vert(data_array,boundary_var,i,0)
        elif S%8==7:
            for i in np.arange(0,L,1):
                for j in np.arange(2,h+1,2):
                    perm_diag_ar(data_array,boundary_var,i,j)
            for i in np.arange(0,L,2):
                perm_vert(data_array,boundary_var,i+1,0)

    return(data_array)

def Global(data_array,rng):
    L, h = data_array.shape
    data_line = data_array.reshape((L*h,1))
    rng.shuffle(data_line)
    data_array = data_line.reshape((L,h))
    return(data_array)

def perm_vert(data_array,boundary_var,i,j):
    L, h = data_array.shape
    if boundary_var == "None":
        if i>=0 and j>=0 and i+1<L and j<h:
            data_array[i,j], data_array[(i+1),j] = data_array[(i+1),j], data_array[i,j]
        else:
            pass
    elif boundary_var == "Periodic":
        data_array[i%L,j%h], data_array[(i+1)%L,j%h] = data_array[(i+1)%L,j%h], data_array[i%L,j%h]
    return(data_array)

def perm_hor(data_array,boundary_var,i,j):
    L, h = data_array.shape
    if boundary_var == "None":
        if i>=0 and j>=0 and i<L and j+1<h:
            data_array[i,j], data_array[i,(j+1)] = data_array[i,(j+1)], data_array[i,j]
        else:
            pass
    elif boundary_var == "Periodic":
        data_array[i%L,j%h], data_array[i%L,(j+1)%h] = data_array[i%L,(j+1)%h], data_array[i%L,j%h]
    return(data_array)

def perm_diag_av(data_array,boundary_var,i,j):
    L, h = data_array.shape
    if boundary_var == "None":
        if i>=1 and j>=0 and i<L and j+1<h:
            data_array[i,j], data_array[i-1,j+1] = data_array[i-1,j+1], data_array[i,j]
        else:
            pass
    elif boundary_var == "Periodic":
        data_array[i%L,j%h], data_array[(i-1)%L,(j+1)%h] = data_array[(i-1)%L,(j+1)%h], data_array[i%L,j%h]
    return(data_array)

def perm_diag_ar(data_array,boundary_var,i,j):
    L, h = data_array.shape
    if boundary_var == "None":
        if i>=1 and j>=1 and i<L and j<h:
            data_array[i,j], data_array[i-1,j-1] = data_array[i-1,j-1], data_array[i,j]
        else:
            pass
    elif boundary_var == "Periodic":
        data_array[i%L,j%h], data_array[(i-1)%L,(j-1)%h] = data_array[(i-1)%L,(j-1)%h], data_array[i%L,j%h]
    return(data_array)