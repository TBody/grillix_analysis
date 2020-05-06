from source import plt
from . import Display

class Plot(Display):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def save_as_svg(self, filename, **kwargs):
        self.style_subplots(**kwargs)
        self.tight_layout()
        plt.savefig(f"{filename}.svg", transparent=True, bbox_inches='tight')
    
    def save_as_png(self, filename, **kwargs):
        self.style_subplots(**kwargs)
        self.tight_layout()
        plt.savefig(f"{filename}.png", transparent=True, bbox_inches='tight')
    
    def fill_values(self, time_slice=slice(-1,None), toroidal_slice=slice(None), poloidal_slice=slice(None)):
        
        for ax in self.axs1d:
            if not ax.assume_frozen and ax.used:
                ax(time_slice=time_slice, toroidal_slice=toroidal_slice, poloidal_slice=poloidal_slice)

        self.add_time_to_title(time_slice)

    def set_data_array(self, run, projector, variables, operators=[]):
        assert(len(variables) <= len(self.axs1d)), f"Requested to plot {len(variables)} variables in {len(self.axs1d)} subplots"

        for variable, ax in zip(variables, self.axs1d):
            ax.set_data(run=run, projector=projector, variable=variable, operators=operators)
    