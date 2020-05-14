from . import CLIArgument

class TimeSlice(CLIArgument):
    def __init__(self, CLI, default_all=False, allow_range=True, allow_step=True):
        super().__init__(CLI, "time_slice")
        self.default_all = default_all
        self.allow_range = allow_range
        self.allow_step = allow_step

        self.parser.add_argument("-t", "--time_slice",
            default=None,
            type=int,
            nargs='+',
            help="Snap index to plot. Leave blank for last snap, give two values for time interval.",
        )
    
    def __call__(self):
        return self.process_slice(self.value, default_all=self.default_all, allow_range=self.allow_range, allow_step=self.allow_step)