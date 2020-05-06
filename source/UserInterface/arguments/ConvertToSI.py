from . import BooleanCLIArgument

class ConvertToSI(BooleanCLIArgument):
    def __init__(self, CLI):
        super().__init__(CLI, "convert_to_SI", default=False)