from source import plt, np
from source.interface import UserEnvironment
from .Axes import Axes

class Figure:

    def __init__(self, **kwargs):
        
        self.fig = plt.figure(**kwargs)
    
    def __getattr__(self, key):
        try:
            return getattr(self.fig, key)
        except AttributeError:
            raise AttributeError(f"{self.__class__.__name__} has no attribute {key}")
    
    def show(self):
        plt.show()
    
    def add_subplots_from_naxs(self, naxs, sharex=True, sharey=True, squeeze=False, subplot_kw=None, gridspec_kw=None):
        [nrows, ncols] = self.determine_layout(naxs)
        self.add_subplots(nrows=nrows, ncols=ncols, sharex=sharex, sharey=sharey, squeeze=False, subplot_kw=subplot_kw, gridspec_kw=gridspec_kw)

    def add_subplots(self, nrows=1, ncols=1, sharex=True, sharey=True, squeeze=False, subplot_kw=None, gridspec_kw=None):
        
        axes = self.fig.subplots(nrows=nrows, ncols=ncols, sharex=sharex, sharey=sharey, squeeze=False, subplot_kw=subplot_kw, gridspec_kw=gridspec_kw)

        self.convert_to_Axes(axes, sharex, sharey)
    
    @property
    def axes1d(self):
        return self.axes.flatten()

    def convert_to_Axes(self, axes, sharex, sharey):
        # Convert from the matplotlib axes object to our own Axes object, which is just a neat wrapper that helps with setting defaults

        axes = np.atleast_2d(axes)
        self.axes = np.empty_like(axes, dtype=Axes)

        for position, ax in np.ndenumerate(axes):
            ax_object = Axes(ax)

            if sharex and (position[1] != 0):
                ax_object.hide_xlabel = True
            if sharey and (position[0] != 0):
                ax_object.hide_ylabel = True
            
            self.axes[position] = ax_object
    
    def make_suptitle(self, text, time=None, **kwargs):
        self._suptitle_base = text
        self._suptitle_time = None
        self._suptitle = plt.suptitle("", **kwargs)
        self.update_suptitle()

    def update_suptitle(self):
        # suptitle_base: this is a string identifier
        # _suptitle_time (float or Quantity): this gives the time corresponding
        # to the data displayed

        if self.suptitle_time is None:
            suptitle_string = f"{self.suptitle_base}"
        elif len(self.suptitle_time) > 1:
            if hasattr(self.suptitle_time[0], "units"):
                suptitle_string = f"{self.suptitle_base} [t={self.suptitle_time[0].to_compact()} to {self.suptitle_time[-1].to_compact()}]"
            else:
                suptitle_string = f"{self.suptitle_base} [time={self.suptitle_time[0]} to {self.suptitle_time[-1]}]"
        else:
            if hasattr(self.suptitle_time[0], "units"):
                suptitle_string = f"{self.suptitle_base} [t={self.suptitle_time.to_compact()}]"
            else:
                suptitle_string = f"{self.suptitle_base} [time={self.suptitle_time}]"
        
        self._suptitle.set_text(suptitle_string)
    
    @property
    def suptitle_base(self):
        return self._suptitle_base
    
    @suptitle_base.setter
    def suptitle_base(self, text):
        self._suptitle_base = text
        self.update_suptitle()
    
    @property
    def suptitle_time(self):
        if self._suptitle_time is None:
            return None
        else:
            return np.atleast_1d(self._suptitle_time)
    
    @suptitle_time.setter
    def suptitle_time(self, time):
        self._suptitle_time = time
        self.update_suptitle()

    def determine_layout(self, naxs):
        if naxs <= 0:
            raise NotImplementedError(f"No figure generated for naxs = {naxs}")
        elif naxs <= 3:
            nrows = 1
            ncols = naxs
        elif naxs == 4:
            nrows = 2
            ncols = 2
        elif naxs <= 6:
            nrows = 2
            ncols = 3
        elif naxs <= 8:
            nrows = 2
            ncols = 4
        elif naxs <= 10:
            nrows = 2
            ncols = 5
        else:
            raise NotImplementedError(f"No figure generated for naxs = {naxs}")
        
        return nrows, ncols
    

