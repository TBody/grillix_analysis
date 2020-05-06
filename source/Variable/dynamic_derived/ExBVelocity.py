from source import np
from source.shared import Vector
from source.Variable.dynamic_derived import DerivedDynamicVariable
from source.Variable.dynamic_base import ElectricField

class ExBVelocity(DerivedDynamicVariable):
    
    def __init__(self, **kwargs):
        self.title = "ExB velocity"
        self.electric_field = ElectricField(**kwargs)
        
        super().__init__(**kwargs)

    def update_normalisation_factor(self):
        self.normalisation_factor = 

    def update_run_values(self):
        self.update_base_variables([self.electric_field])

    def values(self, **kwargs):
        # 1/delta factor for differentiating on R0-normalised grid

        electric_field = self.electric_field(**kwargs)
        

                        
