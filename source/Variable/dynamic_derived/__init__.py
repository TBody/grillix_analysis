from source import np
from source.Variable import Variable

class DerivedDynamicVariable(Variable):
    # Variables which are calculated from combinations of BaseVariables and Operators
    # Does not directly access any NetCDF variable

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def check_base_variables(self, base_variables_list):
        # Should define the following from BaseVariables
        attributes_to_check = ["n_planes", "plane_indices", "n_snaps", 
            "snap_indices", "n_main_grid", "n_perp_grid", "n_full_grid", "grid_points"]

        # Checks each attribute
        for attribute in attributes_to_check:
            for base_variable in base_variables_list:
                if hasattr(self, attribute):
                    # If it's already defined, make sure that all base variables give
                    # the same values
                    assert(np.allclose(getattr(self, attribute), getattr(base_variable, attribute)))
                else:
                    # Otherwise, set the attribute from the current base_variable
                    setattr(self, attribute, getattr(base_variable, attribute))

    def __format_value__(self, value):
        # N.b. may be overwritten by children classes
        
        return f"{value.to_compact():6.4g}"

from .SoundSpeed import SoundSpeed
from .SaturationCurrent import SaturationCurrent
from .FloatingPotential import FloatingPotential
from .AlfvenSpeed import AlfvenSpeed
from .DynamicalPlasmaBeta import DynamicalPlasmaBeta