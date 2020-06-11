from . import BooleanCLIArgument

class CbarInVessel(BooleanCLIArgument):
    def __init__(self, CLI):
        super().__init__(CLI, "cbar_in_vessel", default=True)