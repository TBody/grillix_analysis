from . import CLIArgument

class Group(CLIArgument):
    
    def __init__(self, CLI, group, default):
        super().__init__(CLI, "group")
        assert(default in group), f"Default group {default} must be available in groups {group}"

        self.parser.add_argument("-g", "--group",
                        default=default,
                        type=str,
                        help="Select which group to display",
                        choices=group
                        )