import numpy as np

def fractal(pattern_array,level):
    L = pattern_array.shape[1]
    n = L**level
    patern_level_array = np.zeros((level,n)).astype(np.int8)
    for l in range(1,level+1):
        mask = [pattern_array[0,(i//(L**(l-1)))%L] for i in range(n)]
        patern_level_array[l-1,:] = mask
    init_data_array = np.zeros((1,n))
    init_data_array[0,:] = np.prod(patern_level_array, axis=0)
    return(init_data_array.astype(np.int8))