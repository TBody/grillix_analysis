from . import CLIArgument

class ToroidalSlice(CLIArgument):
    def __init__(self, CLI):
        super().__init__(CLI, "toroidal_slice")
        self.parser.add_argument("-tor", "--toroidal_slice",
            default=None,
            type=int,
            help="Toroidal index. Leave blank to access all planes.",
        )
    
    def __call__(self):
        return self.process_slice(self.value, default_all=True, allow_range=False)