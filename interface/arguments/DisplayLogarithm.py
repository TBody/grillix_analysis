from . import BooleanCLIArgument

class DisplayLogarithm(BooleanCLIArgument):
    def __init__(self, CLI):
        super().__init__(CLI, "display_log", default=False)