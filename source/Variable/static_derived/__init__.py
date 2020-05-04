from source import np, Quantity
from source.Variable import Variable

class DerivedStaticVariable(Variable):
    # Any variable defined in terms of variables written to a metadata file only
    # If a variable consists of any dynamic variable, it should be a DynamicDerivedVariable
    # N.b. the Equilibrium also defines static variables

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

