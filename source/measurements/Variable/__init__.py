from source import Quantity, np, Dimensionless, Component
from ..WrappedArray import ScalarArray, VectorArray, WrappedArray

class Variable(Component):
    # Generic variable container
    # Any field which can be plotted should be of this form
    # Data objects must have a Variable object which matches this pattern
    
    def __init__(self, title, run=None):

        # Every variable must have a title
        self.title = title

        # Attributes which can be overwritten by children. If not already set, set defaults
        
        # continuous_result variables should be treated as having continuous rather than discrete values
        self.continuous_result = getattr(self, "continuous_result", True)
        
        # vector_variable means that the variable has an additional length (3) dimension, which corresponds to (R, phi, Z) components
        self.vector_variable = getattr(self, "vector_variable", False)
        
        # allow_diverging_cmap will make the colormap centre on zero if both positive and negative values are in the range of values
        self.allow_diverging_cmap = getattr(self, "allow_diverging_cmap", True)
        
        # parallel_scalar means that the variable is a scalar which represents a parallel-aligned quantity
        self.parallel_scalar = getattr(self, "parallel_scalar", False)

        # Initialise the run property callbacks
        super().__init__(run=run)
    
    @property
    def normalisation_factor(self):
        # Default to dimensionless quantity (this should be overwritten in child classes)
        return Dimensionless

    def fetch_values(self, time_slice=None, toroidal_slice=None, poloidal_slice=slice(None)):
        raise NotImplementedError(f"{self} has not implemented fetch_values")

    def __call__(self, time_slice=slice(-1,None), toroidal_slice=slice(None), poloidal_slice=slice(None)):
        # Read in the values, and apply the appropriate normalisation factor
        
        values = self.fetch_values(time_slice=time_slice, toroidal_slice=toroidal_slice, poloidal_slice=poloidal_slice)
        units = self.normalisation_factor

        assert (isinstance(values, WrappedArray))
        assert (isinstance(units, Quantity))

        [values, units] = self.values_finalize(values, units)
        values.check_dimensions()

        return values, units
    
    def dimensional_array(self, value_unit_tuple):
        return value_unit_tuple[0] * value_unit_tuple[1]

    def normalised_ScalarArray(self, SI_array):
        # Divide the SI array by the normalisation factor, and assert that the result is dimensionless
        # Then return the ScalarArray and the normalisation_factor
        return ScalarArray((SI_array/self.normalisation_factor).to('').magnitude)
    
    def normalised_VectorArray(self, SI_array):
        # Divide the SI array by the normalisation factor, and assert that the result is dimensionless
        # Then return the VectorArray and the normalisation_factor
        return VectorArray((SI_array/self.normalisation_factor).to('').magnitude)
    
    def __format_value__(self, value):
        # N.b. may be overwritten by children classes
        
        try:
            if isinstance(value, Quantity) and not(self.vector_variable):
                return f"{value.to_compact():6.4g}"
            elif isinstance(value, np.ndarray):
                # Vector result
                assert(np.size(value)==3)
                return f"(R={value[0]:6.4g}, phi={value[1]:6.4g}, Z={value[2]:6.4g})"
            else:
                return f"{value:6.4g}"
        except TypeError:
            print(f"__format_value__ failed for input {value} of type {type(value)}")
            return value

    def values_finalize(self, values, units):
        
        return values, units