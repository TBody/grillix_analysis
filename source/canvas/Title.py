from source import plt, usrenv, np, Dimensionless
from .Axes import AnimatedAxes


class Title(AnimatedAxes):
    axes_extent = usrenv.suptitle_axes_extent

    @classmethod
    def make_title_axes(cls, canvas, **kwargs):
        
        axes = canvas.fig.add_axes(cls.axes_extent, frameon=False)
        axes.set_axis_off()
        
        return cls(axes=axes, **kwargs), axes

    def __init__(self, axes, title_string, SI_units=False, run=None):

        super().__init__(axes)

        self.SI_units = SI_units

        self._suptitle_base = title_string
        self._suptitle_time = None

        [left, bottom, width, height] = self.axes_extent
        right = left + width
        top = bottom + height

        self.artist = self.ax.text(0.5*(left+right), 0.5*(bottom+height), self._suptitle_base, fontsize=usrenv.suptitle_fontsize, horizontalalignment='center',
                      verticalalignment='center', transform=self.ax.transAxes)

        self.run = run
    
    def draw(self, time_slice=slice(-1,None), **kwargs):
        assert(self.initialised)
        
        tau_normalisation = self.normalisation.tau_0 if self.SI_units else Dimensionless
        tau_values = np.atleast_1d(self.run.tau_values[time_slice])*tau_normalisation

        self.suptitle_time = tau_values
    
    def update(self, **kwargs):
        self.draw(**kwargs)

    def clean_frame(self):
        self.artist.set_text("")

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
    
    def update_suptitle(self):
        # suptitle_base: this is a string identifier
        # _suptitle_time (float or Quantity): this gives the time corresponding
        # to the data displayed

        if self.suptitle_time is None:
            suptitle_string = f"{self.suptitle_base}"
        elif len(self.suptitle_time) > 1:
            suptitle_string = f"{self.suptitle_base} [{self.time_units(self.suptitle_time[0])} to {self.time_units(self.suptitle_time[-1])}]"
        else:
            suptitle_string = f"{self.suptitle_base} [{self.time_units(self.suptitle_time[0])}]"
        
        self.artist.set_text(suptitle_string)
    
    def time_units(self, time):

        units = time.units

        if units == "":
            return f"{time.magnitude:4.3f} tau"
        else:
            return f"{time.to_compact():4.3f} tau"

