from source import Quantity, np, Dimensionless
from .. import MComponent
from ..WrappedArray import ScalarArray, VectorArray, WrappedArray

class Variable(MComponent):
    # Generic variable container
    # Any field which can be plotted should be of this form
    # Data objects must have a Variable object which matches this pattern
    
    def __init__(self, title, run=None):

        # Every variable must have a title
        self.title = title

        # Attributes which can be overwritten by children. If not already set, set defaults
        
        # continuous_result variables should be treated as having continuous rather than discrete values
        self.continuous_result = getattr(self, "continuous_result", True)
        
        # # vector_variable means that the variable has an additional length (3) dimension, which corresponds to (R, phi, Z) components
        self.vector_variable = getattr(self, "vector_variable", False)
        
        # # derived_variable means that the normalisation is already applied in the __call__, and so should be skipped
        # self.derived_variable = getattr(self, "derived_variable", False)

        # Initialise the run property callbacks
        super().__init__(run=run)
    
    @property
    def normalisation_factor(self):
        # Default to dimensionless quantity (this should be overwritten in child classes)
        return Dimensionless

    def fetch_values(self, time_slice=None, toroidal_slice=None, poloidal_slice=slice(None)):
        return NotImplemented

    def __call__(self, time_slice=slice(-1,None), toroidal_slice=slice(None), poloidal_slice=slice(None)):
        # Read in the values, and apply the appropriate normalisation factor
        
        [values, units] = self.fetch_values(time_slice=time_slice, toroidal_slice=toroidal_slice, poloidal_slice=poloidal_slice)

        if not(isinstance(values, WrappedArray)):
            if self.vector_variable:
                values = VectorArray(values)
            else:
                values = ScalarArray(values)

        [values, units] = self.values_finalize(values, units)
        values.check_dimensions()

        # if self.SI_units and not(self.derived_variable):
        #     values *= self.normalisation_factor
        # elif not(self.SI_units) and hasattr(values, "units"):
        #     values = values.to('').magnitude
        
        # assert(not(isinstance(values, Result))), f"{self.__class__.__name__} error: Wrapping a Result object in a Result is undefined"
        # if self.vector_variable:
        #     result = VectorResult(values, run=self.run, check_shape=True)
        # else:
        #     result = Result(values, run=self.run, check_shape=True)
        
        # return self.call_finalize(result)
        return values, units
    
#     def __format_value__(self, value):
#         # N.b. may be overwritten by children classes
        
#         try:
#             if isinstance(value, Quantity) and not(self.vector_variable):
#                 return f"{value.to_compact():6.4g}"
#             elif isinstance(value, np.ndarray):
#                 # Vector result
#                 assert(np.size(value)==3)
#                 return f"(R={value[0]:6.4g}, phi={value[1]:6.4g}, Z={value[2]:6.4g})"
#             else:
#                 return f"{value:6.4g}"
#         except TypeError:
#             print(f"__format_value__ failed for input {value} of type {type(value)}")
#             return value

    def values_finalize(self, values, units):
        # Optional function to call before the "Result" is been constructed
        return values, units
    
#     def call_finalize(self, value):
#         # Optional function to call before returning values, after the "Result" has been constructed
#         return value
    
#     def update_base_variables(self, variables):
#         # Passes run to base variable

#         for base_variable in variables:
#             base_variable.run = self.run
    
#     def check_base_variables(self, variables):
#         # Should define the following from BaseVariables
#         attributes_to_check = ["n_planes", "plane_indices", "n_snaps", 
#             "snap_indices", "n_main_grid", "n_perp_grid", "n_full_grid", "grid_points"]

#         # Checks each attribute
#         for attribute in attributes_to_check:
#             for base_variable in variables:

#                 if hasattr(base_variable, attribute):
#                     if hasattr(self, attribute):
#                         # If it's already defined, make sure that all base variables give
#                         # the same values
#                         assert(np.allclose(getattr(self, attribute), getattr(base_variable, attribute)))
#                     else:
#                         # Otherwise, set the attribute from the current base_variable
#                         setattr(self, attribute, getattr(base_variable, attribute))

# from .variable_groups import *