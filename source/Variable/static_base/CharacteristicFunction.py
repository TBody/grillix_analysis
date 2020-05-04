from source.Variable.static_base import PenalisationVariable

class CharacteristicFunction(PenalisationVariable):
    
    def __init__(self, **kwargs):
        
        self.title = "Characteristic"
        super().__init__('pen_chi', **kwargs)
        