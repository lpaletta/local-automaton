import numpy as np

def error_channel(h,L,error_rate,rng):
    new_errors_array = (rng.random((h,L)) < error_rate)
    return(new_errors_array.astype(np.int8))

def get_defect(bidirectional_bool,data_array,meas_error_bool,meas_error_rate,rng):
    h, L = data_array.shape
    defect_array = np.zeros((2 if bidirectional_bool else 1, L), dtype=np.int8)

    # Compute defect array
    base_defect = (data_array != np.roll(data_array, 1))
    if meas_error_bool:
        # Add measurement error
        base_defect = (base_defect + error_channel(h, L, meas_error_rate, rng)) % 2

    defect_array[0, :] = base_defect
    if bidirectional_bool:
        # Add bidirectional defect for future simplified operations between numpy array
        defect_array[1, :] = np.roll(base_defect, -1)

    return(defect_array)

def get_instantaneous_correction(bidirectional_bool,defect_array):
    L = defect_array.shape[1]
    instantaneous_correction_array = np.zeros((1, L), dtype=np.int8)

    if not bidirectional_bool:
        # Correction of (0,1,1) defect substrings
        shifted_r = np.roll(defect_array[0, :], -1)
        shifted_l = np.roll(defect_array[0, :], 1)
        instantaneous_correction_array[0, :] = (shifted_l == 0) * defect_array[0, :] * shifted_r
    else:
        # Correction of (0,1,1) and (1,1,0) defect substrings
        s0 = defect_array[0, :]
        s1 = defect_array[1, :]
        s0_r = np.roll(defect_array[0, :], -1)
        s0_l = np.roll(defect_array[0, :], 1)
        s1_r = np.roll(defect_array[1, :], -1)
        s1_l = np.roll(defect_array[1, :], 1)

        instantaneous_correction_right_array = (s0_l == 0) * s0 * s0_r
        instantaneous_correction_left_array = s1_l * s1 * (s1_r == 0)

        instantaneous_correction_array[0, :] = (instantaneous_correction_right_array + instantaneous_correction_left_array + instantaneous_correction_right_array * instantaneous_correction_left_array) % 2

    return(instantaneous_correction_array.astype(np.int8))

def get_desactivated_defect(bidirectional_bool,defect_array):
    # desactivated defects do not emit signals
    desactivated_defect_array = np.zeros_like(defect_array)

    if bidirectional_bool == False:
        desactivated_defect_array[0,:] = defect_array[0,:]*np.roll(defect_array[0,:],-1)
    if bidirectional_bool == True:
        s0_r = np.roll(defect_array[0,:],-1)
        s1_l = np.roll(defect_array[1,:],1) 
        desactivated_defect_array[0,:] = defect_array[0,:]*s0_r
        desactivated_defect_array[1,:] = defect_array[1,:]*s1_l

    return(desactivated_defect_array.astype(np.int8))

def send_forward_signal(defect_array,forward_signal_array,stack_array):
    forward_signal_array, stack_array = (forward_signal_array + ((forward_signal_array==0)*defect_array))%2, stack_array + ((forward_signal_array==0)*defect_array)
    return(forward_signal_array.astype(np.int8),stack_array.astype(np.int32))

def send_anti_signal(defect_array,anti_signal_array,stack_array):
    anti_signal_array, stack_array = (anti_signal_array + (defect_array==0)*(anti_signal_array==0)*(stack_array>0))%2, stack_array-(defect_array==0)*(anti_signal_array==0)*(stack_array>0)
    return(anti_signal_array.astype(np.int8),stack_array.astype(np.int32))

def correction(defect_array, forward_signal_array, backward_signal_array, bidirectional_bool):
    h, L = defect_array.shape

    if not bidirectional_bool:
        final_correction_array = np.zeros((1,L))
        switch_signal_array = np.zeros((h, L), dtype=np.int8)
        
        final_correction_array[0, :] = np.roll(defect_array[0, :] * forward_signal_array[0, :], -1)
        switch_signal_array = ((np.roll(final_correction_array, 1) + np.roll(final_correction_array, 0))*forward_signal_array[0, :]*(backward_signal_array[0, :]==0))%2
        forward_signal_array[0, :], backward_signal_array[0, :] = (forward_signal_array[0, :] + switch_signal_array) % 2, (backward_signal_array[0, :] + switch_signal_array) % 2

    else:
        final_correction_array = np.zeros((1,L))
        correction_array = np.zeros((h, L), dtype=np.int8)
        correction_dual_array = np.zeros((h, L), dtype=np.int8)
        switch_signal_array = np.zeros((h, L), dtype=np.int8)

        correction_array[0, :] = np.roll(defect_array[0, :] * forward_signal_array[0, :], -1)
        correction_array[1, :] = np.roll(defect_array[1, :] * forward_signal_array[1, :], 1)

        correction_dual_array[0, :] = np.roll(correction_array[0, :], 1)
        correction_dual_array[1, :] = np.roll(correction_array[1, :], -1)

        final_correction_array[0, :] = ((correction_dual_array[1, :] == 0) * correction_array[0, :] +
                                  (correction_dual_array[0, :] == 0) * correction_array[1, :]) % 2
        
        zero_only_correction = (correction_dual_array[1, :] == 0) * correction_array[0, :] #correction proposed only by the upper ASR
        one_only_correction = (correction_dual_array[0, :] == 0) * correction_array[1, :] #correction proposed only by the lower ASR
        conflicted_correction = correction_array[0, :]*correction_dual_array[1, :] #correction proposed by the two ASR

        
        switch_signal_array[0,:] = ((np.roll(zero_only_correction, 1) + np.roll(conflicted_correction, 1) + np.roll(zero_only_correction, 0))*forward_signal_array[0, :]*(backward_signal_array[0, :]==0))%2
        switch_signal_array[1,:] = ((np.roll(one_only_correction, -1) + conflicted_correction + np.roll(one_only_correction, 0))*forward_signal_array[1, :]*(backward_signal_array[1, :]==0))%2

        forward_signal_array, backward_signal_array = (forward_signal_array + switch_signal_array) % 2, (backward_signal_array + switch_signal_array) % 2

    return (final_correction_array.astype(np.int8),
            forward_signal_array.astype(np.int8),
            backward_signal_array.astype(np.int8))

def recombine_signals(forward_signal_array,anti_signal_array):
    mask = forward_signal_array * anti_signal_array
    anti_signal_array, forward_signal_array = (anti_signal_array + mask) % 2, (forward_signal_array + mask) % 2
    return(forward_signal_array.astype(np.int8),anti_signal_array.astype(np.int8))

def recombine_stack(backward_signal_array,stack_array):
    mask = (stack_array>0)*backward_signal_array
    stack_array, backward_signal_array = stack_array - mask, (backward_signal_array + mask)%2
    return(backward_signal_array.astype(np.int8),stack_array.astype(np.int8))

def propagate_signals(bidirectional_bool,forward_signal_array,dx):
    forward_signal_array[0,:] = np.roll(forward_signal_array[0,:],dx)
    if bidirectional_bool == True: #the lower ASR is pointing to the opposite direction
        forward_signal_array[1,:] = np.roll(forward_signal_array[1,:],-dx)
    return(forward_signal_array.astype(np.int8))