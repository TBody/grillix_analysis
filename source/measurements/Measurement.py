from source import np, Quantity
from .MComponent import MComponent
from .Projector import Projector
from .Variable import Variable
from .Operator import Operator, Reduction, ReduceTo1D
from .WrappedArray import WrappedArray, ScalarArray, VectorArray

class Measurement(MComponent):

    def __init__(self, projector, variable, reduction, operators=[], run=None):

        self.projector = projector
        # Operators are applied in list order -- so [f, g, h] will return h(g(f(values))
        # Note that the leftmost operator will be applied first
        self.operators = operators
        self.variable  = variable
        self.reduction = reduction

        # If run is passed, this triggers a callback which sets it on all components
        self.run = run

    def set_run(self):
        # Pass the run object to each sub-object
        run = self.run

        self.projector.run = run
        for operator in self.operators:
            operator.run = run
        self.variable.run = run
        self.reduction.run = run

    def __call__(self, **kwargs):

        # keyword arguments are specific to the projector
        [time_slice, toroidal_slice, poloidal_slice] = self.projector.determine_slices(**kwargs)

        # time_slice, toroidal_slice and poloidal_slice give which values should be fetched from the variable entry in the
        # NetCDF (potentially via several intermediate derived variables)
        [values, units] = self.variable.fetch_values(time_slice=time_slice, toroidal_slice=toroidal_slice, poloidal_slice=poloidal_slice)

        # values is a WrappedArray of shape (times, planes, points) for scalar variables, or of
        # shape (times, planes, points, coordinates) for vector variables
        assert(isinstance(values, WrappedArray))
        # units is a scalar Quantity, which gives the conversion to SI units (otherwise, it is discarded)
        # Therefore, values must give the normalised values, and values * units must give the SI units
        assert(isinstance(units, Quantity))

        # for each operator, operate on the values. Typically, the units will not be changed by the operator,
        # but each operator must explicitly declare that this is the case (i.e. by recieving and returning an
        # unchanged 'units' Quantity)
        # N.b. operators are applied in list order -- i.e. 0th element will be applied first, and so on
        for operator in self.operators:
            [values, units] = operator.operate_on_values(values=values, units=units)

        # The projector assumes a certain data shape, but at this point we have data of shape (times, planes,
        # point, [coordinates])
        # We reduce to the required shape with a reduction operator
        [values, units] = self.reduction.reduce_extra_dimensions(values=values, units=units)

        # We then cast our values into the basis of our projector -- i.e. for cartesian data our projector
        # would define 'x' and 'y', and this step would convert values into a matrix of shape (x, y)
        # This step should not affect the units
        values = self.projector.shape_values(values=values)

        return values, units

    @property
    def projector(self):
        return self._projector

    @projector.setter
    def projector(self, projector):
        if type(projector) == type:
            self._projector = projector()
        else:
            self._projector = projector

        assert(isinstance(self._projector, Projector))

    @property
    def reduction(self):
        return self._reduction

    @reduction.setter
    def reduction(self, reduction):
        if type(reduction) == type:
            self._reduction = reduction()
        else:
            self._reduction = reduction

        if type(self._reduction) == ReduceTo1D:
            self._reduction = self.projector.request_reduction(self._reduction)

        assert(isinstance(self._reduction, Reduction))

    @property
    def operators(self):
        return np.atleast_1d(self._operators)

    @operators.setter
    def operators(self, operators):
        # Shallow copy the list of operators to prevent non-local effects
        operators = operators.copy()
        self._operators = [operator() if type(operator) == type else operator for operator in operators]

        for operator in self._operators:
            assert(isinstance(operator, Operator))

    @property
    def variable(self):
        return self._variable

    @variable.setter
    def variable(self, variable):
        if type(variable) == tuple:
            # Can pass a tuple with ([operators], variable)
            variable = self.split_variable_tuple(variable)

        if type(variable) == type:
            self._variable = variable()
        else:
            self._variable = variable

        assert(isinstance(self._variable, Variable))

    def split_variable_tuple(self, variable_tuple):
        assert((len(variable_tuple) == 2) and (type(variable_tuple[0]) == list)
        ), f"If using the operator-variable tuple notation, must use the form ([operators], variable). variable tuple was {variable_tuple}"

        variable = variable_tuple[1]

        operators = self.operators.copy()
        for operator in variable_tuple[0]:
            # Prepend the operators to the operator list
            # N.b. operators are applied in list order (i.e. 0th first) so the last element of variable_tuple[0] will be the
            # first operator to be applied
            operators.insert(0, operator)

        self.operators = operators

        return variable

