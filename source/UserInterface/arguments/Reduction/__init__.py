from source.UserInterface.arguments import CLIArgument
from source import np

# HANDLED_FUNCTIONS must take arguments axis and keepdims
# 
# To add additional options, implement them here and add them to HANDLED_FUNCTIONS

class Reduction(CLIArgument):

    HANDLED_FUNCTIONS = {
        "mean": np.mean,
        "median": np.median,
        "std": np.std
    }

    def __init__(self, CLI, long_name, description, default="mean"):
        super().__init__(CLI, long_name)
        self.parser.add_argument(f"--{long_name}",
            default=default,
            type=str,
            help=description,
            choices=list(self.HANDLED_FUNCTIONS.keys())
        )
    
    def __call__(self):
        raise NotImplementedError()

from .TimeReduction import TimeReductionArg
from .ToroidalReduction import ToroidalReductionArg
from .PoloidalReduction import PoloidalReductionArg