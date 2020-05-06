from . import CLIArgument

class SnapName(CLIArgument):
    
    def __init__(self, CLI):
        super().__init__(CLI, "snap_name")

        self.parser.add_argument("-sn", "--snap_name",
                        default="snaps",
                        type=str,
                        help="Change snap prefix",
                        choices=["snaps", "error_snaps"]
                        )