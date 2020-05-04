from source import np, Quantity
from .QArray import QArray

HANDLED_FUNCTIONS = {}
def implements(np_function):
    "Register an __array_function__ implementation for QArray objects."
    def decorator(func):
        HANDLED_FUNCTIONS[np_function] = func
        return func
    return decorator

def apply_over_values(function, array, **kwargs):
    print("Here", array, type(array))
    print(QArray.__class__)
    assert(isinstance(array, QArray))
    return array.__class__(
        input_array = function(array.value, **kwargs), normalisation_factor=array.normalisation_factor, convert=array.convert
    )

def function_factory(numpy_function):
    @implements(numpy_function)
    def f(array, **kwargs):
        return apply_over_values(numpy_function, array, **kwargs)

for numpy_function in {np.unique, np.pad, np.nanmax, np.nanmin, np.squeeze}:
    function_factory(numpy_function)

@implements(np.size)
def size(a, array, **kwargs):
    "Implementation of np.size for QArray objects"
    return np.size(a.value, array, **kwargs)

# @implements(np.unique)
# def unique(array, **kwargs):
#     return apply_along_axis(np.unique, array, **kwargs)

# @implements(np.size)
# def unique(array, **kwargs):
#     return apply_along_axis(np.size, array, **kwargs)



# @implements(np.unique)
# def unique(self, array, **kwargs):
#     "Implementation of np.unique for QArray objects"
#     output_array = np.unique(self.value, array, **kwargs)
#     return self.__class__(input_array=output_array, normalisation_factor=self.normalisation_factor, convert=self.convert)

# @implements(np.size)
# def size(a, array, **kwargs):
#     "Implementation of np.size for QArray objects"
#     return np.size(a.value, array, **kwargs)

# @implements(np.pad)
# def pad(array, array, **kwargs):
#     "Implementation of np.pad for QArray objects"
#     output_array = np.pad(array.value, array, **kwargs)
#     return array.__class__(input_array=output_array, normalisation_factor=array.normalisation_factor, convert=array.convert)

# @implements(np.nanmax)
# def nanmax(a, array, **kwargs):
#     "Implementation of np.nanmax for QArray objects"
#     output_array = np.nanmax(a.value, array, **kwargs)
#     return a.__class__(input_array=output_array, normalisation_factor=a.normalisation_factor, convert=a.convert)

# @implements(np.apply_along_axis)
# def apply_along_axis(func1d, axis, arr, array, **kwargs):
#     "Implementation of np.apply_along_axis for QArray objects"
#     # func1d should not change the dimensionality! Otherwise use a different method
#     output_array = np.apply_along_axis(func1d, axis, arr.value, array, **kwargs)
#     return arr.__class__(input_array=output_array, normalisation_factor=arr.normalisation_factor, convert=arr.convert)

# @implements(np.squeeze)
# def squeeze(a, array, **kwargs):
#     "Implementation of np.squeeze for QArray objects"
#     output_array = np.squeeze(a.value, array, **kwargs)
#     return a.__class__(input_array=output_array, normalisation_factor=a.normalisation_factor, convert=a.convert)



# @implements(np.append)
# def append(arr, values, array, **kwargs):
#     "Implementation of np.append for QArray objects"
#     assert(isinstance(arr, QArray))
#     assert(isinstance(values, QArray))
#     assert(arr.normalisation_factor == values.normalisation_factor), f"Cannot append QArrays with different dimensions: {arr.normalisation_factor.units} and {values.normalisation_factor.units}"
#     assert(arr.convert == values.convert)

#     output_array = np.append(arr=arr.value, values=values.value, array, **kwargs)
#     return arr.__class__(input_array=output_array, normalisation_factor=arr.normalisation_factor, convert=arr.convert)

# @implements(np.meshgrid)
# def meshgrid(*xi, **kwargs):
#     value_vector = []
#     for vector in xi:
#         assert(isinstance(vector, QArray))
#         assert(vector.normalisation_factor == vector[0].normalisation_factor)
#         assert(vector.convert == vector[0].convert)
#         value_vector.append(vector.value)
    
#     output_arrays = np.meshgrid(*value_vector, **kwargs)
#     for output_array in output_arrays:
#         output_array = vector[0].__class__(input_array=output_array, normalisation_factor=vector[0].normalisation_factor, convert=vector[0].convert)
    
#     return output_arrays