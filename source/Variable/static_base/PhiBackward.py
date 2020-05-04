from source.Variable.static_base import PenalisationVariable

class PhiBackward(PenalisationVariable):
    
    def __init__(self, **kwargs):
        
        self.title = "Trace against field to plate"
        super().__init__('phi_backward',  **kwargs)
        