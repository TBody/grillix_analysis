from source import np, Quantity
from source.Variable import Result
from pint.numpy_func import HANDLED_FUNCTIONS, implements
# Extends the pint.Quantity class by adding additional supported numpy functions

# Uncomment to show what is supported already
# print(sorted(list(HANDLED_FUNCTIONS)))

@implements("apply_along_axis", "function")
def apply_along_axis(func1d, axis, arr, *args, **kwargs):
    assert(isinstance(arr, (Quantity, Result)))
    return Quantity(np.apply_along_axis(func1d, axis, arr.magnitude, *args, **kwargs), arr.units)

