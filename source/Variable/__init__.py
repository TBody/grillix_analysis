from source import Quantity, np
from .Result import Result, VectorResult

class Variable():
    # Generic variable container
    # Any field which can be plotted should be of this form
    # Data objects must have a Variable object which matches this pattern
    
    def __init__(self, run=None):
        
        # Attributes which can be overwritten by children. If not already set, set defaults
        # Default to dimensionless value
        self.normalisation_factor = getattr(self, "normalisation_factor", Quantity(1, ''))
        # display_linear will prevent the variable from converting to logarithmic
        self.display_linear = getattr(self, "display_linear", False)
        # numerical_variable means that the variable can be operated on
        self.numerical_variable = getattr(self, "numerical_variable", True)
        # vector_variable means that the variable has an additional length (3) dimension, which corresponds to (R, phi, Z) components
        self.vector_variable = getattr(self, "vector_variable", False)
        # derived_variable means that the normalisation is already applied in the __call__, and so should be skipped
        self.derived_variable = getattr(self, "derived_variable", False)

        # Call run at the end, since this triggers a 'set' routine which may depend on the default values
        self.run = run

    from source.shared.properties import (update_run_values, update_normalisation_factor, run, convert)

    def values(self, time_slice=None, toroidal_slice=None, poloidal_slice=slice(None)):
        return NotImplemented

    def __call__(self, time_slice=slice(-1,None), toroidal_slice=slice(None), poloidal_slice=slice(None)):
        # Read in the values, and apply the appropriate normalisation factor
        
        values = self.values(time_slice=time_slice, toroidal_slice=toroidal_slice, poloidal_slice=poloidal_slice)
        values = self.values_finalize(values)

        if self.convert and not(self.derived_variable):
            values *= self.normalisation_factor
        elif not(self.convert) and hasattr(values, "units"):
            values = values.to('').magnitude
        
        assert(not(isinstance(values, Result))), f"{self.__class__.__name__} error: Wrapping a Result object in a Result is undefined"
        if self.vector_variable:
            result = VectorResult(values, run=self.run, check_shape=True)
        else:
            result = Result(values, run=self.run, check_shape=True)
        
        return self.call_finalize(result)
    
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

    def values_finalize(self, value):
        # Optional function to call before the "Result" is been constructed
        # Usually a reshape such as np.atleast_3d(values).reshape((1,1,-1))
        return value
    
    def call_finalize(self, value):
        # Optional function to call before returning values, after the "Result" has been constructed
        return value
    
    def update_base_variables(self, variables):
        # Passes run to base variable

        for base_variable in variables:
            base_variable.run = self.run
    
    def check_base_variables(self, variables):
        # Should define the following from BaseVariables
        attributes_to_check = ["n_planes", "plane_indices", "n_snaps", 
            "snap_indices", "n_main_grid", "n_perp_grid", "n_full_grid", "grid_points"]

        # Checks each attribute
        for attribute in attributes_to_check:
            for base_variable in variables:

                if hasattr(base_variable, attribute):
                    if hasattr(self, attribute):
                        # If it's already defined, make sure that all base variables give
                        # the same values
                        assert(np.allclose(getattr(self, attribute), getattr(base_variable, attribute)))
                    else:
                        # Otherwise, set the attribute from the current base_variable
                        setattr(self, attribute, getattr(base_variable, attribute))

from .variable_groups import *