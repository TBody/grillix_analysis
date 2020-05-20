from . import CLIArgument

class Filepath(CLIArgument):
    def __init__(self, CLI):
        super().__init__(CLI, "filepath")
        self.parser.add_argument("-f", "--filepath",
            required=True, type=str,
            help="Full filepath to top-level run directory."
        )