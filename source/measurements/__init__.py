from source import np
from .Measurement import Measurement
from .WrappedArray import WrappedArray, ScalarArray, VectorArray

def measurement_array_from_variable_array(projector, variable_array, reduction, operators=[], run=None):
    variable_array = np.atleast_1d(variable_array)
    assert(variable_array.ndim == 1)

    measurement_array = np.empty_like(variable_array, dtype=Measurement)

    for i in range(variable_array.size):
        measurement_array[i] = Measurement(projector=projector, variable=variable_array[i], reduction=reduction, operators=operators, run=run)

    return measurement_array