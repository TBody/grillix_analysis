from . import CLIArgument

class TimeSlice(CLIArgument):
    def __init__(self, CLI):
        super().__init__(CLI, "time_slice")
        self.parser.add_argument("-t", "--time_slice",
            default=None,
            type=int,
            nargs='+',
            help="Snap index to plot. Leave blank for last snap, give two values for time interval.",
        )
    
    def __call__(self):
        return self.process_slice(self.value, default_all=False, allow_range=True)