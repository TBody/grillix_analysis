from source import np, Quantity
from pint.numpy_func import HANDLED_FUNCTIONS, implements

# Extends the pint.Quantity class by adding additional supported numpy functions

@implements("apply_along_axis", "function")
def apply_along_axis(func1d, axis, arr, *args, **kwargs):
    assert(isinstance(arr, Quantity))
    return Quantity(np.apply_along_axis(func1d, axis, arr.magnitude, *args, **kwargs), arr.units)

