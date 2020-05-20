from source import plt, np
from source.interface import UserEnvironment
from .Subplot import Subplot

class Display:

    def __init__(self, nrows=None, ncols=None, naxs=None, run=None, sharex=True, sharey=True, maximised=True, title=None, convert=False, log_scale=False, **kwargs):
        
        self.determine_layout(nrows, ncols, naxs)

        self.run = run
        self.title = title
        self.SI_units = convert
        self.log_scale = log_scale

        kwargs = self.set_kwargs_from_user_environment(maximised, kwargs)

        self.fig, axs = plt.subplots(self.nrows, self.ncols, sharex=sharex, sharey=sharey, **kwargs)

        # Make the axs array into a 2D array
        axs = np.array(axs)
        if self.nrows == 1:
            axs = np.expand_dims(axs, axis=0)
        if self.ncols == 1:
            axs = np.expand_dims(axs, axis=-1)
        assert(axs.ndim == 2)
        
        self.axs = np.zeros((self.nrows, self.ncols), dtype=Subplot)
        # Convert the axes into "Subplot" objects
        for row in range(self.nrows):
            for col in range(self.ncols):
                self.axs[row][col] = Subplot(self, axs[row][col])
        
        self.axs1d = self.axs.flatten()
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
        
        self.suptitle_text = self.suptitle.get_text()
        
    def set_data_array(self, run, projector, variables, operators=[]):
        assert(len(variables) <= len(self.axs1d)), f"Requested to plot {len(variables)} variables in {len(self.axs1d)} subplots"

        for variable, ax in zip(variables, self.axs1d):
            ax.set_data(run=run, projector=projector, variable=variable, operators=operators)
    
    def fill_values(self, time_slice=slice(-1,None), toroidal_slice=slice(None), poloidal_slice=slice(None), add_time_to_title=True):
        
        for ax in self.axs1d:
            if not ax.assume_frozen and ax.used:
                ax(time_slice=time_slice, toroidal_slice=toroidal_slice, poloidal_slice=poloidal_slice)

        if add_time_to_title:
            self.add_time_to_title(time_slice)
    
    def add_time_to_title(self, time_slice):
        
        try:
            tau_values = np.atleast_1d(self.run.tau_values[time_slice])

            if len(tau_values) > 1:
                if self.SI_units:
                    self.suptitle.set_text(f"{self.suptitle_text} [t = {tau_values[0].to_compact():4.3f} to {tau_values[-1].to_compact():4.3f}]")
                else:
                    self.suptitle.set_text(f"{self.suptitle_text} [{tau_values[0]:4.3f} to {tau_values[-1]:4.3f} tau]")
            else:
                if self.SI_units:
                    self.suptitle.set_text(f"{self.suptitle_text} [t = {tau_values[0].to_compact():4.3f}]")
                else:
                    self.suptitle.set_text(f"{self.suptitle_text} [{tau_values[0]:4.3f} tau]")
        except AttributeError:
            print("Cannot add time to title")
    
    @property
    def run(self):
        return self._run

    @run.setter
    def run(self, value):
        self._run = value
    
    def determine_layout(self, nrows, ncols, naxs):

        if not(nrows is None) and not(ncols is None):
            self.nrows = nrows
            self.ncols = ncols
            assert(naxs is None), (f"{self.__class__.__name__} error: incompatible arguments. "
                "Should supply either nrows(={nrows}) and ncols(={ncols}), or naxs(={naxs}), but not both")
        else:
            assert((not(naxs) is None) and (nrows is None) and (ncols is None)), (f"{self.__class__.__name__} error: incompatible arguments. "
                "Should supply either nrows(={nrows}) and ncols(={ncols}), or naxs(={naxs}), but not both or neither")

            if naxs <= 0:
                raise NotImplementedError(f"No figure generated for naxs = {naxs}")
            elif naxs <= 3:
                self.nrows = 1
                self.ncols = naxs
            elif naxs == 4:
                self.nrows = 2
                self.ncols = 2
            elif naxs <= 6:
                self.nrows = 2
                self.ncols = 3
            elif naxs <= 8:
                self.nrows = 2
                self.ncols = 4
            elif naxs <= 10:
                self.nrows = 2
                self.ncols = 5
            else:
                raise NotImplementedError(f"No figure generated for naxs = {naxs}")
    
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
        for ax in self.axs1d:
            ax.style_plot(**kwargs)
    
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