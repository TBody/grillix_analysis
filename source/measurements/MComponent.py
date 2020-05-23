class MComponent():
    # Generic measurement element -- i.e. an operator, variable or projector -- 
    # or the Measurement itself

    def __init__(self, run=None):
        
        self.run = run

    def set_run(self):
        # Dummies, should be overwritten
        pass

    @property
    def initialised(self):
        if self.run == None:
            return False
        else:
            return True

    @property
    def run(self):
        try:
            return self._run
        except AttributeError:
            return None

    @run.setter
    def run(self, value):
        self._run = value
        if value != None:
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
    
    def __repr__(self):
        repr_string = ""

        for superclass in (self.__class__.__mro__)[-2::-1]:
            # Print the inheritance pattern for the object
            repr_string += superclass.__name__ + "::"
        
        # Strip the last ::
        repr_string = repr_string[:-2]

        # Add initialised flag
        repr_string += f" initialised={self.initialised}"

        return repr_string