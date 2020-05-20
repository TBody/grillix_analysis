class MComponent():
    # Generic measurement element -- i.e. an operator, variable or projector -- 
    # or the Measurement itself

    def __init__(self, run=None):
        
        self.run = run

    def set_run(self):
        # Dummies, should be overwritten
        # print(f"self {self} called set_run")
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
            self.set_run()

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

    @property
    def normalisation(self):
        return self.run.normalisation