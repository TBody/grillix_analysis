from source import np, Quantity
from source.Variable import Variable

class DerivedDynamicVariable(Variable):
    # Variables which are calculated from combinations of BaseVariables and Operators
    # Does not directly access any NetCDF variable

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def check_base_variables(self, variables):
        # Should define the following from BaseVariables
        attributes_to_check = ["n_planes", "plane_indices", "n_snaps", 
            "snap_indices", "n_main_grid", "n_perp_grid", "n_full_grid", "grid_points"]

        # Checks each attribute
        for attribute in attributes_to_check:
            for base_variable in variables:

                base_variable.run = self.run

                if hasattr(self, attribute):
                    # If it's already defined, make sure that all base variables give
                    # the same values
                    assert(np.allclose(getattr(self, attribute), getattr(base_variable, attribute)))
                else:
                    # Otherwise, set the attribute from the current base_variable
                    setattr(self, attribute, getattr(base_variable, attribute))

from .SoundSpeed import SoundSpeed
from .AlfvenSpeed import AlfvenSpeed
from .DynamicalPlasmaBeta import DynamicalPlasmaBeta
from .ElectricField import ElectricField
from .FloatingPotential import FloatingPotential
from .SaturationCurrent import SaturationCurrent