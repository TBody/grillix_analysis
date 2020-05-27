from source import usrenv
from .Axes import AnimatedAxes
from .Colorbar import Colorbar
from .Painter import Painter
from matplotlib import animation

def update(self, **kwargs):
    for axes in self.axes:
        if isinstance(axes, AnimatedAxes):
            axes.update(**kwargs)

def clean_frame(self):
    for axes in self.axes:
        if isinstance(axes, AnimatedAxes):
            axes.clean_frame()

def find_static_colormap(self, **kwargs):
    for axes in self.axes:
        if isinstance(axes, Colorbar):
            axes.find_static_colormap(**kwargs)

def return_animation_artists(self):
    animation_artists = []
    
    for axes in self.axes:
        if isinstance(axes, AnimatedAxes):
            animation_artists.append(axes.artist)
        
        if isinstance(axes, Painter):
            animation_artists += axes.annotations
    
    for artist in animation_artists:
        assert(hasattr(artist, "set_animated"))

    return animation_artists

def make_animator(self, run, time_slice, toroidal_slice):

    # First, we iterate over all of the snaps to find the limits of the colormap
    sparse_time_slice = slice(time_slice.start, time_slice.stop, usrenv.sparse_time_slice)
    self.find_static_colormap(time_slice=sparse_time_slice, toroidal_slice=toroidal_slice)
    
    # Then, determine which planes actually correspond to the given time_slice
    snap_indices = run.snap_indices[time_slice]

    # Draw the first frame
    self.draw(time_slice=snap_indices[0], toroidal_slice=toroidal_slice)
    self.tight_layout()
    
    def make_clean_frame():
        # import ipdb; ipdb.set_trace()
        self.clean_frame()
        return self.return_animation_artists()

    # Make a function which animates the next frames
    def animate(t):
        print(f"\tMaking frame {t} of [{snap_indices[0]}-{snap_indices[-1]}]")
        self.update(time_slice=[t], toroidal_slice=toroidal_slice)
        
        return self.return_animation_artists()
    
    # Build the 'animator' which plots each frame
    self.animator = animation.FuncAnimation(self.fig, animate, init_func=make_clean_frame, frames=snap_indices, blit=True, repeat = True)
    
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