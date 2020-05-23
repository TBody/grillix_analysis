class MComponent():
    # Generic measurement element -- i.e. an operator, variable or projector -- 
    # or the Measurement itself

    def __init__(self, run=None):
        
        self.run = run

    def set_run(self):
        # Dummies, should be overwritten
        pass

    @property
    def run(self):
        return self._run

    @run.setter
    def run(self, value):
        if value != None:
            self._run = value
            self.set_run()

    @property
    def SI_units(self):
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