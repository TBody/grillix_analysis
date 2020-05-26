from . import BooleanCLIArgument

class ExcludeOutliers(BooleanCLIArgument):
    def __init__(self, CLI):
        super().__init__(CLI, "exclude_outliers", default=False)