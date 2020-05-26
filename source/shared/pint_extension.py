from source import np, Quantity

# Add WrappedArray properties
@property
def vector_magnitude(quantity):
    return Quantity(quantity.magnitude.vector_magnitude, quantity.units)

@property
def R(quantity):
    return Quantity(quantity.magnitude.R, quantity.units)
    
@property
def phi(quantity):
    return Quantity(quantity.magnitude.phi, quantity.units)

@property
def Z(quantity):
    return Quantity(quantity.magnitude.Z, quantity.units)

Quantity.vector_magnitude = vector_magnitude
Quantity.R = R
Quantity.phi = phi
Quantity.Z = Z