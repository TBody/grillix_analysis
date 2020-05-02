from source import plt, np
from source.shared import UserEnvironment
from .Subplot import Subplot

class Display:

    def __init__(self, nrows=1, ncols=1, sharex=True, sharey=True, maximised=True, title=None, time_in_title=True, SI_conversion=False, display_logarithmic=False, **kwargs):

        self.nrows = nrows
        self.ncols = ncols
        self.title = title
        self.SI_conversion = SI_conversion
        self.display_logarithmic = display_logarithmic

        kwargs = self.set_kwargs_from_user_environment(maximised, kwargs)

        self.fig, axs = plt.subplots(nrows, ncols, sharex=sharex, sharey=sharey, **kwargs)

        # Make the axs array into a 2D array
        axs = np.array(axs)
        if nrows == 1:
            axs = np.expand_dims(axs, axis=0)
        if ncols == 1:
            axs = np.expand_dims(axs, axis=-1)
        assert(axs.ndim == 2)
        
        self.axs = np.zeros((nrows, ncols), dtype=Subplot)
        # Convert the axes into "Subplot" objects
        for row in range(self.nrows):
            for col in range(self.ncols):
                self.axs[row][col] = Subplot(self, axs[row][col])
        # Rearrange the axs array such that indexing is [x, y]
        self.axs = np.transpose(np.flipud(self.axs))
        
        for position, ax in np.ndenumerate(self.axs):
            if sharex and (position[1] != 0):
                ax.hide_xlabel = True
            if sharey and (position[0] != 0):
                ax.hide_ylabel = True
        
        if self.title:
            self.suptitle = plt.suptitle(self.title)
        else:
            self.suptitle = plt.suptitle("")
    
    def set_kwargs_from_user_environment(self, maximised, kwargs):

        usrenv = UserEnvironment()

        if 'dpi' not in kwargs:
            kwargs['dpi'] = usrenv.default_figure_resolution
        
        if 'figsize' not in kwargs:
            if maximised:
                kwargs['figsize'] = (usrenv.screen_dimension_x/kwargs['dpi'], usrenv.screen_dimension_y/kwargs['dpi'])
            else:
                kwargs['figsize'] = (usrenv.default_figure_size_x/kwargs['dpi'], usrenv.default_figure_size_y/kwargs['dpi'])
        
        return kwargs
    
    def style_subplots(self, **kwargs):
        for x in range(self.ncols):
            for y in range(self.nrows):
                self.axs[x][y].style_plot(**kwargs)
    
    def tight_layout(self):
        plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    def show(self, **kwargs):
        self.style_subplots(**kwargs)
        self.tight_layout()
        plt.show()
    
    def close(self):
        plt.close(self.fig)

from .Plot import Plot
from .Animate import Animate