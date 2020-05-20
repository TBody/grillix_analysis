from . import CLIArgument

class Title(CLIArgument):
    def __init__(self, CLI):
        super().__init__(CLI, "title")
        self.parser.add_argument("--title",
            default=None,
            type=str,
            help="Set the title for the resulting plot"
        )
    
    def __call__(self):
        if self.value:
            return self.value
        else:
            return self.args.filepath