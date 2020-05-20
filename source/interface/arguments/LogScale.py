from . import BooleanCLIArgument

class LogScale(BooleanCLIArgument):
    def __init__(self, CLI):
        super().__init__(CLI, "log_scale", default=False)