from source import np
# Don't make a custom class -- want to keep numpy array and pint.Quantity functionality intact
# Instead, this provides a simple routine to convert from 3 [time, plane, poloidal_index] arrays 
# to a [time, plane, poloidal_index, vector_index] array
# 
# Assumed indexing is [R, phi, Z]

def vector_like(array_shape, R_array, Z_array, phi_array=None):
    vector_array = np.empty(tuple(list(array_shape)+[3]))
    
    assert(R_array.shape == array_shape)
    vector_array[..., 0] = R_array
    
    if phi_array == None:
        vector_array[..., 1] = np.zeros(array_shape)
    else:
        assert(phi_array.shape == array_shape)
        vector_array[..., 1] = phi_array
    
    assert(Z_array.shape == array_shape)
    vector_array[..., 2] = Z_array

    return vector_array
