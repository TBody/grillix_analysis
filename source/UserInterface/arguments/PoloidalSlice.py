from . import CLIArgument

class PoloidalSlice(CLIArgument):
    def __init__(self, CLI):
        super().__init__(CLI, "poloidal_slice")
        self.parser.add_argument("-pol", "--poloidal_slice",
            default="all",
            type=str,
            help="Poloidal slice to plot -- default is all, can supply single ",
            choices=["all", "closed", "SOL", "in_vessel"]
        )
    
    def __call__(self):
        raise NotImplementedError()