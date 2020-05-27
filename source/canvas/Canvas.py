from source import np, plt, Dimensionless, usrenv
from .Painter import Painter, PoloidalPlot
from .Colorbar import Colorbar
# from .. import Component
# from .Figure import Figure
# from .Axes import Axes
# from .painter import Painter, PoloidalPlot
# from source.measurements import Measurement
# import matplotlib.animation as animation

class Canvas:
    # Similar to matplotlib.figure, with extended methods to allow easier plotting and animation

    def __init__(self, **kwargs):
        self.fig = plt.figure(**kwargs)

    def show(self):
        plt.show()
    
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
    
    def __getattr__(self, key):
        try:
            return getattr(self.fig, key)
        except AttributeError:
            raise AttributeError(f"{self.__class__.__name__} has no attribute {key}")

    def subplots_from_naxs(self, naxs, sharex=True, sharey=True, squeeze=False, subplot_kw=None, gridspec_kw=None):
        [nrows, ncols] = self.determine_layout(naxs)
        return self.subplots(nrows=nrows, ncols=ncols, sharex=sharex, sharey=sharey, squeeze=False, subplot_kw=subplot_kw, gridspec_kw=gridspec_kw)

    def subplots(self, nrows=1, ncols=1, sharex=True, sharey=True, squeeze=False, subplot_kw=None, gridspec_kw=None):
        return self.fig.subplots(nrows=nrows, ncols=ncols, sharex=sharex, sharey=sharey, squeeze=False, subplot_kw=subplot_kw, gridspec_kw=gridspec_kw)
    
    def subplots_from_measurement_array(self, painter, measurement_array, run=None, SI_units=False, log_scale=False, exclude_outliers=False, **subplot_kw):
        assert(type(painter) is type)

        subplots = self.subplots_from_naxs(naxs=len(measurement_array), **subplot_kw)
        self.axes = []

        for measurement, subplot in zip(measurement_array, subplots.flatten()):

            painter_object = painter(axes=subplot, measurement=measurement, run=run, SI_units=SI_units)
            cbar_object, _ = Colorbar.make_colorbar_axis(painter=painter_object, run=run, log_scale=log_scale, exclude_outliers=exclude_outliers)

            self.axes.append(painter_object)
            self.axes.append(cbar_object)
    
    def draw(self, with_tight_layout=True, **kwargs):
        
        for axes in self.axes:
            axes.draw(**kwargs)
        
        # self.add_time_to_title(**kwargs)

        if with_tight_layout:
            # Leave space for the suptitle
            plt.tight_layout(rect=[0, 0, 1, 1-usrenv.suptitle_spacing])


# class Canvas(Component):

#     def __init__(self, figure, run=None):
#         self.figure = figure
#         self.run = run

#     @classmethod
#     def blank_canvas(cls):
#         return cls(figure=Figure())
    
#     @property
#     def fig(self):
#         return self.figure.fig

#     def draw(self, with_tight_layout=True, **kwargs):
#         for axes in self.axes_array:
#             axes.draw(**kwargs)
        
#         # self.add_time_to_title(**kwargs)

#         if with_tight_layout:
#             # Leave space for the suptitle
#             plt.tight_layout(rect=[0, 0, 1, 0.95])
    
#     def update(self, **kwargs):
#         for axes in self.axes_array:
#             axes.update(**kwargs)
        
#         # self.add_time_to_title(**kwargs)
#         # self.figure._suptitle.set_text("Hello")
#         # plt.suptitle("Hello")
#         # self.figure._suptitle.set_text("Hello")
#         # self.figure._suptitle.draw()
    
#     def clean_frame(self):
#         for axes in self.axes_array:
#             axes.clean_frame()
        
#         # self.figure._suptitle.set_text("")
    
#     def find_static_colormap_normalisations(self, **kwargs):
#         for axes in self.axes_array:
#             axes.painter.find_static_colormap_normalisation(**kwargs)

#     def show(self):
#         self.figure.show()

#     def add_subplots_from_naxs(self, naxs):
#         self.figure.add_subplots_from_naxs(naxs=naxs)
#         self.axes_array = self.figure.axes1d

#     def add_title(self, title, title_SI=False):
#         self.title_text = title
#         self.title_SI = title_SI
#         self.figure.make_suptitle(self.title_text)
    
#     def add_time_to_title(self, time_slice=slice(-1,None), **kwargs):
#         tau_normalisation = self.normalisation.tau_0 if self.title_SI else Dimensionless
#         tau_values = np.atleast_1d(self.run.tau_values[time_slice])*tau_normalisation

#         self.figure.suptitle_time = tau_values
    
#     def associate_subplots_with_measurements(self, painter, measurement_array, SI_units=False, log_scale=False, exclude_outliers=False):

#         for measurement, axes in zip(measurement_array, self.axes_array):

#             axes.painter = painter(canvas=self, measurement=measurement, axes=axes, SI_units=SI_units, log_scale=log_scale, exclude_outliers=exclude_outliers)
        
#     def set_SI_units(self, value):
#         for axes in self.axes_array:
#             axes.SI_units = value
    
#     def set_log_scale(self, value):
#         for axes in self.axes_array:
#             axes.log_scale = value
    
#     def save_figure(self, filename):
#         plt.savefig(f"{filename}", transparent=True)
    
#     def return_animation_artists(self):
#         animation_artists = []
        
#         for axes in self.axes_array:
#             artist = axes.return_artist()
#             if artist:
#                 animation_artists.append(artist)
        
#         # animation_artists.append(self.figure._suptitle)
        
#         return animation_artists
    
#     def make_animator(self, frames, animation_function):
#         self.animator = animation.FuncAnimation(self.fig, animation_function, frames=frames, blit=False, repeat = True)
    
#     def save_animation(self, filename):
#         animation_kwargs = {
#         "fps": usrenv.animation_framerate,
#         "metadata": dict(artist=usrenv.author_name),
#         "bitrate": usrenv.animation_bitrate,
#         "codec": usrenv.animation_codec
#         }

#         if usrenv.animation_writer == "FFMpegFileWriter":
#             # Saves temporary figures to disk, then stiches them together
#             # Slower, but better memory handling
#             writer = animation.FFMpegFileWriter(**animation_kwargs)
#         elif usrenv.animation_writer == "FFMpegWriter":
#             # Stores images in memory, then stiches together.
#             # May be faster, but could result in out-of-memory issues for large animations
#             writer = animation.FFMpegWriter(**animation_kwargs)
#         else:
#             print(f"Warning: writer {usrenv.animation_writer} not implemented. Falling back to FFMpegFileWriter")
#             writer = animation.FFMpegFileWriter(**animation_kwargs)
        
#         animation_filename = filename.with_suffix('.'+usrenv.animation_format)

#         print(f"Saving video as {animation_filename}")
#         self.animator.save(animation_filename, writer=writer, dpi=usrenv.animation_dpi)
#         print("Done")