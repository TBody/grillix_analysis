def update_run_values(self):
    # Dummies, should be overwritten
    # print(f"self {self} called update_run_values")
    pass

def update_normalisation_factor(self):
    # Dummies, should be overwritten
    # print(f"self {self} called update_normalisation_factor")
    pass

@property
def run(self):
    # print(f"self {self} called run")
    return self._run

@run.setter
def run(self, value):
    # print(f"self {self} called run with arg {value}")
    if value != None:
        self._run = value
        self._run.add_to_children(self)
        
        self.update_run_values()

        self.normalisation = value.normalisation
        self.update_normalisation_factor()

@property
def SI_units(self):
    # print(f"self {self} called SI_units")
    try:
        return self._run.SI_units
    except AttributeError:
        # If run isn't defined yet, assume call is before initialisation. Return default
        return False

@SI_units.setter
def SI_units(self, value):
    assert(self.run.SI_units == value)
    raise NotImplementedError(f"Should set SI_units directly on run")