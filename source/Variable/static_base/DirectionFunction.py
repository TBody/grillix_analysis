from source.Variable.static_base import PenalisationVariable

class DirectionFunction(PenalisationVariable):
    
    def __init__(self, **kwargs):
        
        self.title = "Plate direction"
        super().__init__('pen_xi',  **kwargs)
        