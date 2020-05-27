from source import Dimensionless

@property
def projector(self):
    return self.measurement.projector

@property
def variable(self):
    return self.measurement.variable

@property
def x_values(self):
    return self.measurement.projector.x * self.x_normalisation

@property
def y_values(self):
    return self.measurement.projector.y * self.y_normalisation

@property
def x_normalisation(self):
    if self.SI_units:
        return self.measurement.projector.x_normalisation
    else:
        return Dimensionless

@property
def y_normalisation(self):
    if self.SI_units:
        return self.measurement.projector.y_normalisation
    else:
        return Dimensionless