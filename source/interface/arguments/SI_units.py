from . import BooleanCLIArgument

class SI_units(BooleanCLIArgument):
    def __init__(self, CLI):
        super().__init__(CLI, "SI_units", default=False)