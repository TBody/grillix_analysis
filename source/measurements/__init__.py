from source import np
from .Measurement import Measurement
from .WrappedArray import WrappedArray, ScalarArray, VectorArray

def measurement_array_from_variable_array(projector, variable_array, reduction, operators=[], run=None):
    assert(type(variable_array) is list)

    measurement_array = np.empty((len(variable_array)), dtype=Measurement)

    for i in range(len(variable_array)):
        measurement_array[i] = Measurement(projector=projector, variable=variable_array[i], reduction=reduction, operators=operators, run=run)

    return measurement_array