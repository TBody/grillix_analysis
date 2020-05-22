from . import CLIArgument

class Reduction(CLIArgument):

    def __init__(self, CLI, default="mean"):
        from source.measurements.Operator.Reduction import reduction_functions

        self.reduction_functions = reduction_functions

        super().__init__(CLI, "reduction")
        self.parser.add_argument(f"--reduction",
            default=default,
            type=str,
            help="Function to reduce z to a single dimension",
            choices=list(self.reduction_functions.keys())
        )
    
    def __call__(self):
        from source.measurements.Operator.Reduction import ReduceTo1D

        return ReduceTo1D(self.reduction_functions[self.value])