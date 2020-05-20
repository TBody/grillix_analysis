from . import PenalisationVariable

class PhiForward(PenalisationVariable):
    
    def __init__(self, **kwargs):
        
        self.title = "Trace with field to plate"
        super().__init__('phi_forward',  **kwargs)
        