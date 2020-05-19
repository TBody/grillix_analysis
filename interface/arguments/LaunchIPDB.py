from . import BooleanCLIArgument

class LaunchIPDB(BooleanCLIArgument):
    def __init__(self, CLI):
        super().__init__(CLI, "launch_ipdb", default=False)