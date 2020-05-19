from . import BooleanCLIArgument

class ErrorSnaps(BooleanCLIArgument):
    def __init__(self, CLI):
        super().__init__(CLI, "error_snaps", default=False)