from source import np, plt, Dimensionless, usrenv
from .. import Component
from .layout import Figure, Axes
from .painter import Painter, PoloidalPlot
from source.measurements import Measurement
import matplotlib.animation as animation

# def _blit_draw(self, artists, bg_cache):
#     # Handles blitted drawing, which renders only the artists given instead
#     # of the entire figure.
#     updated_ax = []
#     for a in artists:
#         # If we haven't cached the background for this axes object, do
#         # so now. This might not always be reliable, but it's an attempt
#         # to automate the process.
#         if a.axes not in bg_cache:
#             # bg_cache[a.axes] = a.figure.canvas.copy_from_bbox(a.axes.bbox)
#             # change here
#             bg_cache[a.axes] = a.figure.canvas.copy_from_bbox(a.axes.figure.bbox)
#         a.axes.draw_artist(a)
#         updated_ax.append(a.axes)

#     # After rendering all the needed artists, blit each axes individually.
#     for ax in set(updated_ax):
#         # and here
#         # ax.figure.canvas.blit(ax.bbox)
#         ax.figure.canvas.blit(ax.figure.bbox)

# # MONKEY PATCH!!
# matplotlib.animation.Animation._blit_draw = _blit_draw

class Canvas(Component):

    def __init__(self, figure, run=None):
        self.figure = figure
        self.run = run

    @classmethod
    def blank_canvas(cls):
        return cls(figure=Figure())
    
    @property
    def fig(self):
        return self.figure.fig

    def draw(self, with_tight_layout=True, **kwargs):
        for axes in self.axes_array:
            axes.draw(**kwargs)
        
        # self.add_time_to_title(**kwargs)

        if with_tight_layout:
            # Leave space for the suptitle
            plt.tight_layout(rect=[0, 0, 1, 0.95])
    
    def update(self, **kwargs):
        for axes in self.axes_array:
            axes.update(**kwargs)
        
        # self.add_time_to_title(**kwargs)
        # self.figure._suptitle.set_text("Hello")
        # plt.suptitle("Hello")
        # self.figure._suptitle.set_text("Hello")
        # self.figure._suptitle.draw()
    
    def clean_frame(self):
        for axes in self.axes_array:
            axes.clean_frame()
        
        # self.figure._suptitle.set_text("")
    
    def find_static_colormap_normalisations(self, **kwargs):
        for axes in self.axes_array:
            axes.painter.find_static_colormap_normalisation(**kwargs)

    def show(self):
        self.figure.show()

    def add_subplots_from_naxs(self, naxs):
        self.figure.add_subplots_from_naxs(naxs=naxs)
        self.axes_array = self.figure.axes1d

    def add_title(self, title, title_SI=False):
        self.title_text = title
        self.title_SI = title_SI
        self.figure.make_suptitle(self.title_text)
    
    def add_time_to_title(self, time_slice=slice(-1,None), **kwargs):
        tau_normalisation = self.normalisation.tau_0 if self.title_SI else Dimensionless
        tau_values = np.atleast_1d(self.run.tau_values[time_slice])*tau_normalisation

        self.figure.suptitle_time = tau_values
    
    def associate_subplots_with_measurements(self, painter, measurement_array, SI_units=False, log_scale=False, exclude_outliers=False):

        for measurement, axes in zip(measurement_array, self.axes_array):

            axes.painter = painter(canvas=self, measurement=measurement, axes=axes, SI_units=SI_units, log_scale=log_scale, exclude_outliers=exclude_outliers)
        
    def set_SI_units(self, value):
        for axes in self.axes_array:
            axes.SI_units = value
    
    def set_log_scale(self, value):
        for axes in self.axes_array:
            axes.log_scale = value
    
    def save_figure(self, filename):
        plt.savefig(f"{filename}", transparent=True)
    
    def return_animation_artists(self):
        animation_artists = []
        
        for axes in self.axes_array:
            artist = axes.return_artist()
            if artist:
                animation_artists.append(artist)
        
        # animation_artists.append(self.figure._suptitle)
        
        return animation_artists
    
    def make_animator(self, frames, animation_function):
        self.animator = animation.FuncAnimation(self.fig, animation_function, frames=frames, blit=False, repeat = True)
    
    def save_animation(self, filename):
        animation_kwargs = {
        "fps": usrenv.animation_framerate,
        "metadata": dict(artist=usrenv.author_name),
        "bitrate": usrenv.animation_bitrate,
        "codec": usrenv.animation_codec
        }

        if usrenv.animation_writer == "FFMpegFileWriter":
            # Saves temporary figures to disk, then stiches them together
            # Slower, but better memory handling
            writer = animation.FFMpegFileWriter(**animation_kwargs)
        elif usrenv.animation_writer == "FFMpegWriter":
            # Stores images in memory, then stiches together.
            # May be faster, but could result in out-of-memory issues for large animations
            writer = animation.FFMpegWriter(**animation_kwargs)
        else:
            print(f"Warning: writer {usrenv.animation_writer} not implemented. Falling back to FFMpegFileWriter")
            writer = animation.FFMpegFileWriter(**animation_kwargs)
        
        animation_filename = filename.with_suffix('.'+usrenv.animation_format)

        print(f"Saving video as {animation_filename}")
        self.animator.save(animation_filename, writer=writer, dpi=usrenv.animation_dpi)
        print("Done")