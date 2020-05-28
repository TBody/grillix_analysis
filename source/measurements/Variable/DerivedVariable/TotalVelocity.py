from source import np, unit_registry
from . import DerivedVariable, ExBVelocity
from ..BaseVariable import ParallelIonVelocity
from source.measurements.Operator import VectorParallel

class TotalVelocity(DerivedVariable):
    
    def __init__(self, run=None):
        title = "Total Velocity"
        self.ion_velocity = ParallelIonVelocity()
        self.exb_velocity = ExBVelocity()
        self.vector_parallel = VectorParallel()

        self.base_variables = [self.ion_velocity, self.exb_velocity, self.vector_parallel]
        
        super().__init__(title, run=None)

    @property
    def normalisation_factor(self):
        return self.normalisation.c_s0.to('kilometers/second')

    def fetch_values(self, **kwargs):
        # To understand what exactly is going on in the next line is a bit tricky
        # First, we call self.ion_velocity with the keyword arguments **kwargs, which give the requested slice
        # This returns (values, units) as a tuple
        # We then pass values, units to self.vector_parallel, where the asterisk expands the tuple
        # i.e. function(*(values, units)) == function(values, units)
        # Finally, we capture the (values, units) returned and pack them into an Quantity array which
        # has SI units

        ion_velocity = self.dimensional_array(self.vector_parallel(*self.ion_velocity(**kwargs)))
        exb_velocity = self.dimensional_array(self.exb_velocity(**kwargs))

        total_velocity = ion_velocity + exb_velocity

        return self.normalised_VectorArray(total_velocity)
