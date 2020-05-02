from source import np
from source.Variable import Variable

class DerivedStaticVariable(Variable):
    # Any variable defined in terms of variables written to a metadata file only
    # If a variable consists of any dynamic variable, it should be a DynamicDerivedVariable
    # N.b. the Equilibrium also defines static variables

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __format_value__(self, value, SI_conversion, **kwargs):
        # N.b. may be overwritten by children classes
        if SI_conversion:
            return f"{value.to_compact():6.4g}"
        else:
            return f"{value:6.4g}"
