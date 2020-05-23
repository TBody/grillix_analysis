from source import Component

class RunComponent(Component):

    def __init__(self, run):
        assert(run != None), f"{self} requires a run object to be provided"
        self.run = run
