from . import Operator
from source import np
from ..WrappedArray import VectorArray

class PerpendicularGradient(Operator):
    
    def __init__(self, run=None):
        super().__init__(run=run)
    
    def __call__(self, values, units):
        
        # Should only be operated on scalar fields. For vector fields either do component-wise or implement new operator
        assert(not(values.is_vector))
        # Convert to 2D matrix
        shaped_values = self.run.grid.vector_to_matrix(values)

        # Calculate the gradient. Units should be correctly propagated (including 1/m for the gradient)
        raise NotImplementedError()
        # Should add a factor of delta on the values, and 1/delta 1/m on units
        gradient_R = np.gradient(shaped_values, self.run.grid.grid_spacing, axis=-1)
        gradient_Z = np.gradient(shaped_values, self.run.grid.grid_spacing, axis=-2)

        # Convert back to 1D vectors
        gradient_R = self.run.grid.matrix_to_vector(gradient_R)
        gradient_Z = self.run.grid.matrix_to_vector(gradient_Z)

        return VectorArray.poloidal(R_array=gradient_R, Z_array=gradient_Z), units