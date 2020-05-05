from source import np, Quantity
from numbers import Number

class Result():

    from source.shared.properties import (update_run_values, update_normalisation_factor, run, convert)

    def __init__(self, values, source_variable, run=None, check_shape=False):
        # Don't convert to np.array -- since this will strip units if passed a Quantity
        self.values = values
        if check_shape:
            assert(self.check_dimensions()), f"{self.__class__.__name__} called with shape {self.values.shape}"

        self.variable = source_variable
        self.run = run

    def __str__(self):
        return f"{self.__class__.__name__} {self.values}"

    def __getattr__(self, key):
        # If an attribute is requested that returns an AttributeError, try query the values instead
        return getattr(self.values, key)
    
    def __array__(self):
        return self.values
    
    def check_dimensions(self):
        return (self.values.ndim == 3)
    
    @property
    def is_vector(self):
        return getattr(self, "_vector", False)

    @property
    def z(self):
        # Return values for plotting
        if isinstance(self.values, Quantity):
            return self.values.magnitude
        elif isinstance(self.values, np.ndarray):
            return self.values
        else:
            raise NotImplementedError()
    
    def __getitem__(self, key):
        # Allows natural subscripting (i.e. Result[x, y])
        return self.values[key]
    
    def __array_ufunc__(self, ufunc, method, *args, **kwargs):
        
        if self.single_type_argument(args):
            args = self.downcast_args_to_values(args)
            output = self.values.__array_ufunc__(ufunc, method, *args, **kwargs)
            # print(f"__array_ufunc__ called with \n\tself={self}, \n\tufunc={ufunc}, \n\tmethod={method}, \n\targs={args}, \n\tkwargs={kwargs}, \n\toutput={output}\n")
            return self.rewrap_output(output)
        else:
            raise NotImplementedError()
    
    def single_type_argument(self, args):
        # Check whether special handling is required for the __array_function__
        result_types_in_args = 0
        for arg in args:
            if isinstance(arg, Result):
                result_types_in_args += 1
        if result_types_in_args <= 1:
            return True
        else:
            return False

    def downcast_args_to_values(self, args, types=[]):
        # Replace Result with values

        new_types = []
        new_args  = []

        for arg in args:
            if isinstance(arg, Result):
                new_args.append(arg.values)
                new_types.append(type(arg.values))
            else:
                new_args.append(arg)

        for t in types:
            if not(issubclass(t, Result)):
                new_types.append(t)

        if types:
            return tuple(new_args), tuple(new_types)
        else:
            return tuple(new_args)

    def __array_function__(self, func, types, args, kwargs):

        if self.single_type_argument(args):
            args, types = self.downcast_args_to_values(args, types)
            output = self.values.__array_function__(func, types, args, kwargs)
            # print(f"__array_function__ called with \n\tself={self}, \n\tfunc={func}, \n\ttypes={types}, \n\targs={args}, \n\tkwargs={kwargs}, \n\toutput={output}")
            return self.rewrap_output(output)
        else:
            raise NotImplementedError()
    
    def rewrap_output(self, output):
        if isinstance(output, Number):
            return output
        elif (isinstance(output, np.ndarray) or isinstance(output, Quantity)):
            return self.__class__(values=output, source_variable=self.variable, run=self.run)
        else:
            raise NotImplementedError(f"No implementation for wrapping output of type {type(output)}")

class VectorResult(Result):

    @classmethod
    def poloidal_init_from_subarrays(cls, R_array, Z_array, source_variable, run=None):
        vector_array = cls.poloidal_vector_from_subarrays(R_array=R_array, Z_array=Z_array)
        
        return cls(vector_array=vector_array, source_variable=source_variable, run=run)
    
    @classmethod
    def init_from_subarrays(cls, R_array, phi_array, Z_array, source_variable, run=None):
        vector_array = cls.vector_from_subarrays(R_array=R_array, Z_array=Z_array, phi_array=phi_array)
        
        return cls(vector_array=vector_array, source_variable=source_variable, run=run)

    @classmethod
    def poloidal_vector_from_subarrays(cls, R_array, Z_array):

        if isinstance(R_array, Quantity) or isinstance(Z_array, Quantity):
            assert(isinstance(R_array, Quantity) and isinstance(Z_array, Quantity))
            
            # Convert to compatible units -- will raise an error if not possible
            if not(Z_array.units == R_array.units):
                Z_array = Z_array.to(R_array.units)
            phi_array = Quantity(np.zeros(R_array.shape), R_array.units)
        else:
            phi_array = np.zeros(R_array.shape)
        
        return cls.vector_from_subarrays(R_array=R_array, phi_array=phi_array, Z_array=Z_array)

    @classmethod
    def vector_from_subarrays(cls, R_array, phi_array, Z_array):
        
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
    
    def check_dimensions(self):
        return ((self.values.ndim == 4) and (self.values.shape[-1] == 3))

    def __init__(self, values, source_variable, run=None, check_shape=False):
        
        self._vector = True
        super().__init__(values=values, source_variable=source_variable, run=run, check_shape=check_shape)