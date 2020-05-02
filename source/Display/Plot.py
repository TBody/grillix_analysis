from source import plt
from . import Display

class Plot(Display):
    
    def __init__(self, nrows=1, ncols=1, **kwargs):
        super().__init__(nrows=nrows, ncols=ncols, **kwargs)
    
    def save_as_svg(self, filename, **kwargs):
        self.style_subplots(**kwargs)
        self.tight_layout()
        plt.savefig(f"{filename}.svg", transparent=True, bbox_inches='tight')
    
    def save_as_png(self, filename, **kwargs):
        self.style_subplots(**kwargs)
        self.tight_layout()
        plt.savefig(f"{filename}.png", transparent=True, bbox_inches='tight')
    
    def fill_values(self, time_slice=slice(-1,None), toroidal_slice=slice(None), poloidal_slice=slice(None)):
        
        for x in range(self.ncols):
            for y in range(self.nrows):
                if not self.axs[x][y].assume_frozen:
                    self.axs[x][y].fill_values(time_slice, toroidal_slice, poloidal_slice)