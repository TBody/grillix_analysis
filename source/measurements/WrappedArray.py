from source import np, Quantity

class WrappedArray(np.ndarray):
    # A very boring ndarray subclass
    # Behaves exactly like an ndarray, except for some extra methods
    # and a flag which identifies if it is a vector array (i.e.
    # unstructured is 4D = [time, planes, points, component]) or 
    # not (i.e. unstructured is 3D = [time, planes, points])
    # 
    # However, subclassing ndarrays is a bit tricky (see https://numpy.org/devdocs/user/basics.subclassing.html)
    # so we leave the comments in

    def __new__(cls, input_array):
        # Input array is an already formed ndarray instance
        # We first cast to be our class type
        obj = np.asarray(input_array).view(cls)
        # Finally, we must return the newly created object:
        return obj

    def __array_finalize__(self, obj):
        # ``self`` is a new object resulting from
        # ndarray.__new__(WrappedArray, ...), therefore it only has
        # attributes that the ndarray.__new__ constructor gave it -
        # i.e. those of a standard ndarray.
        #
        # We could have got to the ndarray.__new__ call in 3 ways:
        # From an explicit constructor - e.g. WrappedArray():
        #    obj is None
        #    (we're in the middle of the WrappedArray.__new__
        #    constructor, and self.info will be set when we return to
        #    WrappedArray.__new__)
        if obj is None: return
        # From view casting - e.g arr.view(WrappedArray):
        #    obj is arr
        #    (type(obj) can be WrappedArray)
        # From new-from-template - e.g infoarr[:3]
        #    type(obj) is WrappedArray
        #
        # We do not need to return anything
    
    @property
    def is_vector(self):
        if isinstance(self, VectorArray):
            return True
        else:
            return False
    
    def check_dimensions(self):
        # Should only be checked before structuring with a Projector
        if self.is_vector:
            assert(self.ndim == 4)
            assert(self.len_coords == 3)
        else:
            assert(self.ndim == 3)
    
    @property
    def dim_time(self):
        return 0
    
    @property
    def dim_phi(self):
        return 1
    
    @property
    def dim_points(self):
        return 2

    @property
    def len_time(self):
        return self.shape[self.dim_time]
    
    @property
    def len_phi(self):
        return self.shape[self.dim_phi]
    
    @property
    def len_points(self):
        return self.shape[self.dim_points]

class ScalarArray(WrappedArray):
    pass

class VectorArray(WrappedArray):

    @property
    def dim_coords(self):
        return 3
    
    @property
    def len_coords(self):
        return self.shape[self.dim_coords]

    @classmethod
    def poloidal(cls, R_array, Z_array):
        vector_array = cls.poloidal_vector(R_array=R_array, Z_array=Z_array)
        
        return cls.__new__(cls, vector_array)
    
    @classmethod
    def cylindrical(cls, R_array, phi_array, Z_array):
        vector_array = cls.vector(R_array=R_array, Z_array=Z_array, phi_array=phi_array)
        
        return cls.__new__(cls, vector_array)

    @classmethod
    def poloidal_vector(cls, R_array, Z_array):

        if isinstance(R_array, Quantity) or isinstance(Z_array, Quantity):
            assert(isinstance(R_array, Quantity) and isinstance(Z_array, Quantity))
            
            # Convert to compatible units -- will raise an error if not possible
            if not(Z_array.units == R_array.units):
                Z_array = Z_array.to(R_array.units)
            phi_array = Quantity(np.zeros(R_array.shape), R_array.units)
        else:
            phi_array = np.zeros(R_array.shape)
        
        return cls.cylindrical_vector(R_array=R_array, phi_array=phi_array, Z_array=Z_array)

    @classmethod
    def cylindrical_vector(cls, R_array, phi_array, Z_array):
        
        subarrays = [R_array, phi_array, Z_array]
        array_shape = R_array.shape

        vector_array = np.empty(tuple(list(array_shape)+[3]))
        units = getattr(R_array, "units", None)
        
        if isinstance(R_array, Quantity) or isinstance(Z_array, Quantity) or isinstance(phi_array, Quantity):
            assert(isinstance(R_array, Quantity) and isinstance(Z_array, Quantity) and isinstance(phi_array, Quantity))

        for i, subarray in enumerate(subarrays):
            assert(subarray.shape == array_shape)
            if units != None:
                # Convert to compatible units -- will raise an error if not possible -- and extract magnitudes
                subarrays[i] = (subarray.to(units)).magnitude

        vector_array[..., 0] = subarrays[0] #R_array
        vector_array[..., 1] = subarrays[1] #phi_array
        vector_array[..., 2] = subarrays[2] #Z_array

        if units != None:
            vector_array = Quantity(vector_array, units)

        return vector_array
    
    @property
    def vector_magnitude(self):
        return ScalarArray(np.linalg.norm(self, axis=-1))
    
    @property
    def R(self):
        return ScalarArray(self.values[...,0])
    
    @property
    def phi(self):
        return ScalarArray(self.values[...,1])

    @property
    def Z(self):
        return ScalarArray(self.values[...,2])
    
    def dot_product(self, other):
        return ScalarArray(np.sum(np.multiply(self, other), axis=-1))