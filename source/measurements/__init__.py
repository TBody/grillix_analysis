from source import np
from .MComponent import MComponent
from .Projector import Projector
from .Variable import Variable
from .Operator import Operator
from .WrappedArray import WrappedArray, ScalarArray, VectorArray

class Measurement(MComponent):

    def __init__(self, projector, variable, operators=[]):
        
        self.projector = projector
        self.operators = operators
        self.variable  = variable
        
        operators = [operator() if type(operator) == type else operator for operator in operators]
    
    @property
    def projector(self):
        return self._projector
    
    @projector.setter
    def projector(self, value):
        if type(value) == type:
            self._projector = value()
        else:
            self._projector = value
        
        assert(isinstance(self._projector, Projector))
    
    @property
    def operators(self):
        return np.atleast_1d(self._operators)
    
    @operators.setter
    def operators(self, values):
        # Shallow copy the list of values to prevent non-local effects
        values = values.copy()
        self._operators = [operator() if type(operator) == type else operator for operator in values]
        
        for operator in self._operators:
            assert(isinstance(operator, Operator))
    
    @property
    def variable(self):
        return self._variable
    
    @variable.setter
    def variable(self, value):
        if type(value) == tuple:
            # Can pass a tuple with ([operators], variable)
            value = self.split_variable_tuple(value)

        if type(value) == type:
            self._variable = value()
        else:
            self._variable = value
        
        assert(isinstance(self._variable, Variable))
    
    def split_variable_tuple(self, variable_tuple):
        assert((len(variable_tuple) == 2) and (type(variable_tuple[0]) == list)
        ), f"If using the operator-variable tuple notation, must use the form ([operators], variable). variable tuple was {variable_tuple}"

        variable = variable_tuple[1]
        
        operators = self.operators.copy()
        for operator in variable_tuple[0]:
            # Prepend the operators to the operator list
            # N.b. operators are applied in list order (i.e. 0th first) so the last element of variable_tuple[0] will be applied first
            operators.insert(0, operator)
        
        self.operators = operators

        return variable

