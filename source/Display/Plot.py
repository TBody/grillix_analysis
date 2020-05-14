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