from source.Variable.StaticVariable import PenalisationVariable

class PhiBetweenTargets(PenalisationVariable):
    
    def __init__(self, **kwargs):
        
        self.title = "Trace between targets"
        super().__init__('phi_between_targets',  **kwargs)
        