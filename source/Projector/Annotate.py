class Annotate:

    def __init__(self, run=None):
        
        if run != None:
            self.set_run(run)
    
    def set_run(self, run, projector):
        self.run = run
        self.normalisation = run.normalisation
        self.projector = projector

        if hasattr(self, "set_normalisation_factor"):
            self.set_normalisation_factor()
        
        if hasattr(self, "set_values_from_run"):
            self.set_values_from_run()
    
    def __call__(self, subplot, linestyle='-', linewidth=0.5):
        pass

    def style_plot(self, subplot):
        pass