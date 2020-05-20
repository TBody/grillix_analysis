from source import np
class CLIArgument:

    def __init__(self, CLI, name):
        self.CLI = CLI
        self.name = name
        self.CLI.argument_dictionary[self.name] = self

    @property
    def parser(self):
        return self.CLI.parser
    
    @property
    def args(self):
        assert(self.CLI.initialised)
        return self.CLI.args
    
    @property
    def value(self):
        return getattr(self.args, self.name, None)
    
    def __call__(self):
        # Override to process value in children
        return self.value
    
    @staticmethod
    def process_value(value):
        # To correctly slice with negative indices, including endpoints
        if value == -1:
            return None
        elif value < 0:
            return value + 1
        else:
            return value
    
    def process_slice(self, slice_argument, default_all=True, allow_range=False, allow_step=True):
        # N.b. call to slice is slice(start, stop, step). Supplying less than 3 arguments gives
        #   1. slice(stop)
        #   2. slice(start, stop)
        #   3. slice(start, stop, step)
        # 
        # Default values are None. This translates to
        #   stop = None: index to end
        #   start = None: index from start
        #   step = None: take every element
        # 
        result = NotImplemented
        
        if slice_argument is None:
            if default_all:
                # Take all values
                result = slice(None)
            else:
                # Take the last value
                result = slice(-1, None)
        else:
            slice_argument = np.atleast_1d(slice_argument)

            if len(slice_argument) == 1:
                # Take a single value
                value = self.process_value(slice_argument[0])
                if value is None:
                    # Take all the values
                    result = slice(None)
                elif value < 0:
                    # Take a single element slice
                    result = slice(value-1, value)
                else:
                    # Take a single element slice
                    result = slice(value, value+1)

            elif (len(slice_argument) == 2):
                if allow_range:
                    # Slice between start (1st argument) and stop (2nd argument)
                    result = slice(self.process_value(slice_argument[0]), self.process_value(slice_argument[1]))
                elif allow_step:
                    # Slice up to stop (1st argument), taking steps of step (2nd argument)
                    result = slice(None, self.process_value(slice_argument[0]), self.process_value(slice_argument[1]))
            
            elif (len(slice_argument) == 3) and (allow_range and allow_step):
                # Slice between start (1st argument) and stop (2nd argument), in steps of step (3rd argument)
                result = slice(self.process_value(slice_argument[0]), self.process_value(slice_argument[1]), self.process_value(slice_argument[2]))

        if result is NotImplemented:
            raise NotImplementedError(f"{self.__class__.__name__} called with value {slice_argument}")
        
        return result

class BooleanCLIArgument(CLIArgument):

    def __init__(self, CLI, name, default=False):

        super().__init__(CLI, name)

        self.add_bool_arg(name, default=default)
    
    def add_bool_arg(self, name, default=False):
        
        group = self.parser.add_mutually_exclusive_group(required=False)
        group.add_argument('--' + name, dest=name, action='store_true')
        group.add_argument('--no_' + name, dest=name, action='store_false')
        self.parser.set_defaults(**{name:default})

# Add Arg to the name, to prevent Namespace muddling
from .Filepath         import Filepath         as FilepathArg
from .SaveFilepath     import SaveFilepath     as SaveFilepathArg
from .Group            import Group            as GroupArg
from .Title            import Title            as TitleArg
from .TimeSlice        import TimeSlice        as TimeSliceArg
from .ToroidalSlice    import ToroidalSlice    as ToroidalSliceArg
from .PoloidalSlice    import PoloidalSlice    as PoloidalSliceArg
from .SI_units         import SI_units         as SI_unitsArg
from .LogScale         import LogScale         as LogScaleArg
from .LaunchIPDB       import LaunchIPDB       as LaunchIPDBArg
from .ErrorSnaps       import ErrorSnaps       as ErrorSnapsArg
from .Reduction import *