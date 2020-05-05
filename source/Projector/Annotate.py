class Annotate:

    def __init__(self, run=None):
        self.initialised = False
        self.run = run
    
    from source.shared.properties import (update_normalisation_factor, run, convert)

    def update_run_values(self):
        self.initialised = True
    
    def __call__(self, subplot, linestyle='-', linewidth=0.5):
        pass

    def style_plot(self, subplot):
        pass