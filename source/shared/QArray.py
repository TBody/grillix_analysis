from source import Quantity, np
from . import Vector
import numpy.lib.mixins
from numbers import Number

# See https://numpy.org/doc/stable/user/basics.dispatch.html#basics-dispatch
# https://numpy.org/doc/stable/reference/generated/numpy.lib.mixins.NDArrayOperatorsMixin.html#numpy.lib.mixins.NDArrayOperatorsMixin

unitless = Quantity(1, '')

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
        input_array = function(array.value, **kwargs), normalisation_factor=array.normalisation_factor, SI_conversion=array.SI_conversion
    )

def function_factory(numpy_function):
    @implements(numpy_function)
    def f(array, **kwargs):
        return apply_over_values(numpy_function, array, **kwargs)

for numpy_function in {np.unique, np.pad, np.nanmax, np.nanmin, np.squeeze}:
    function_factory(numpy_function)

@implements(np.size)
def size(array, **kwargs):
    "Implementation of np.size for QArray objects"
    return np.size(array.value, **kwargs)

class QArray(np.lib.mixins.NDArrayOperatorsMixin):

    @classmethod
    def init_poloidal(cls, input_array, *args, **kwargs):
        input_array = np.asarray(input_array)
        assert(input_array.ndim == 1)
        input_array = (np.atleast_3d(input_array)).reshape((1,1,-1))
        return cls(input_array, *args, **kwargs)

    def __init__(self, input_array, normalisation_factor=unitless, SI_conversion=False):
        self.value = np.asarray(input_array)
        self.normalisation_factor = normalisation_factor
        self.SI_conversion = SI_conversion
    
    def set_SI_conversion(self, value):
        setattr(self, "SI_conversion", value)
    
    def dimensionless(self):
        if self.SI_conversion or self.normalisation_factor.dimensionless:
            return True
        else:
            return False
    
    def __repr__(self):
        if self.SI_conversion:
            return f"{self.__class__.__name__} [{self.normalisation_factor}] => {self.value}"
        else:
            return f"{self.__class__.__name__} [{self.normalisation_factor}] /> {self.value}"
    
    def __array__(self):
        if self.SI_conversion:
            return self.value*self.normalisation_factor
        else:
            return self.value
    
    def __float__(self):
        if self.normalisation_factor.dimensionless:
            if self.SI_conversion:
                return float(self.value*self.normalisation_factor)
            else:
                return float(self.value)
        else:
            raise RuntimeError(f"{self.__class__.__name__}.__float__ called on array with dimensions [{self.normalisation_factor.units}]. Use magnitude to strip units")
    
    def __len__(self):
        return np.size(self.value)
    
    def __getitem__(self, key):
        return self.__class__(input_array=self.value[key], normalisation_factor=self.normalisation_factor, SI_conversion=self.SI_conversion)
    
    def __getattr__(self, key):
        # If an attribute is requested which isn't available in QArray, try search the ndarray attributes
        
        if (key == "units"):
            return self.normalisation_factor.units if self.SI_conversion else ''
        elif hasattr(self.value, key):
            return self.value.__getattribute__(key)
        else:
            raise AttributeError(f"No attribute '{key}' found in {self.__class__.__name__} or np.ndarray")
    
    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        print(f"ufunc={ufunc}, method={method}, inputs={inputs}, kwargs={kwargs}\n")
        if method == '__call__':
            
            scalars = []
            norm_factor = []

            for element in inputs:

                if isinstance(element, Number):
                    scalars.append(element)
                    norm_factor.append(unitless)

                elif isinstance(element, Quantity):
                    scalars.append(element.magnitude)
                    norm_factor.append(Quantity(1, element.units))

                elif isinstance(element, self.__class__):
                    scalars.append(element.value)
                    norm_factor.append(element.normalisation_factor)
                    assert(self.SI_conversion == element.SI_conversion), f"{self.__class__.__name__} error: Inconsistent application of SI_conversion"

                elif isinstance(element, list):
                    element = np.asarray(element)
                    scalars.append(element)
                    norm_factor.append(unitless)
                
                elif isinstance(element, np.ndarray):
                    element = np.asarray(element)
                    scalars.append(element)
                    norm_factor.append(unitless)

                else:
                    raise NotImplementedError(f"{self.__class__.__name__} called with ufunc={ufunc}, method={method}, kwargs={kwargs}: no implementation for element {element}, type {type(element)}")
            
            return self.__class__(ufunc(*scalars, **kwargs),
                                  normalisation_factor=ufunc(*norm_factor, **kwargs),
                                  SI_conversion=self.SI_conversion)
        else:
            raise NotImplementedError(f"{self.__class__.__name__} called with ufunc={ufunc}, method={method}, inputs={inputs}, kwargs={kwargs}")

    def __array_function__(self, func, types, args, kwargs):
        if func not in HANDLED_FUNCTIONS:
            return NotImplemented

        # print("self", self)
        # print("func", func)
        # print("types", types)
        # print("args", args)
        # print("kwargs", kwargs)

        # Note: this allows subclasses that don't override
        # __array_function__ to handle QArray objects.
        if not all(issubclass(t, self.__class__) for t in types):
            return NotImplemented
        return HANDLED_FUNCTIONS[func](*args, **kwargs)

    def to_compact(self):
        assert(self.value.size == 1)
        if self.SI_conversion:
            return (self.value*self.normalisation_factor).to_compact()
        else:
            return self.value
    
    def to_base_units(self):
        assert(self.value.size == 1)
        if self.SI_conversion:
            return (self.value*self.normalisation_factor).to_base_units()
        else:
            return self.value

class VectorQArray(QArray):
    
    def __init__(self):
        pass

# class QArray(np.ndarray):
#     # Array of values with units
    
#     def __new__(cls, input_array, normalisation_factor=Quantity(1, '')):
#         # Input array is an already formed ndarray instance
#         # We first cast to be our class type
#         obj = np.asarray(input_array).view(cls)
#         if obj.ndim == 1:
#             obj = np.atleast_3d(obj).reshape((1,1,-1))
#         # add the new attribute to the created instance
#         obj.normalisation_factor = normalisation_factor
#         obj.SI_conversion = None
#         # Finally, we must return the newly created object:
#         return obj

#     def __array_finalize__(self, obj):
#         if obj is None: return
#         self.normalisation_factor = getattr(obj, 'normalisation_factor', None)
#         self.SI_conversion = getattr(obj, 'SI_conversion', None)

#     def set_SI_conversion(self, value):
#         assert(type(value) == bool)
#         setattr(self, "SI_conversion", value)
    
#     def __getattr__(self, key):
#         if key == "units":
#             return self.normalisation_factor.units
#         # elif key == "magnitude":
#         #     return self.magnitude()
#         # elif key == "values":
#         #     return self.values()
#         else:
#             return super().__getattr__(key)

#     def magnitude(self):
#         if self.SI_conversion:
#             return self*self.normalisation_factor.magnitude
#         else:
#             return self
    

#     # def array_to_compact(array):
#     #     if hasattr(array, "units"):
#     #         array = array.to(
#     #             (np.mean(array)
#     #             ).to_compact().units)
#     #     return array

# class VectorQArray(QArray):

#     def __new__(cls, input_array, normalisation_factor=Quantity(1, '')):
#         # Input array is an already formed ndarray instance
#         # We first cast to be our class type
#         obj = np.asarray(input_array, dtype=Vector).view(cls)
#         # add the new attribute to the created instance
#         obj.normalisation_factor = normalisation_factor
#         obj.SI_conversion = None
#         # Finally, we must return the newly created object:
#         return obj

#     def __array_finalize__(self, obj):
#         if obj is None: return
#         self.normalisation_factor = getattr(obj, 'normalisation_factor', None)
#         self.SI_conversion = getattr(obj, 'SI_conversion', None)
    
#     @classmethod
#     def from_component_arrays(cls, R, Z, phi, **kwargs):
#         assert(R.shape == Z.shape)
#         assert(R.shape == phi.shape)

#         vector_array = np.empty_like(R, dtype=Vector)

#         for vector, r, z, p in zip(vector_array, R, Z, phi):

#             vector = Vector(R=r, Z=z, phi=p)

#         cls(vector_array, **kwargs)
