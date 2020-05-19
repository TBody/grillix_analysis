from source import np, plt
from . import Display
from matplotlib import animation
from source.shared import UserEnvironment

class Animate(Display):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setup_animation(self, time_slice=slice(None), toroidal_slice=slice(None), poloidal_slice=slice(None), save=False):
        
        # Read the tau values to determine how many snaps to plot
        snap_indices = self.run.snap_indices[time_slice]
        
        axes = []

        def init_animation():
            for ax in self.axs1d:
                if not ax.assume_frozen and ax.used:
                    print(f"Finding colormap limits for {ax.variable.title}")
                    ax.find_colormap_limits(time_slice=time_slice, toroidal_slice=toroidal_slice, poloidal_slice=poloidal_slice)
                    ax(time_slice=snap_indices[0], toroidal_slice=toroidal_slice, poloidal_slice=poloidal_slice, update=False)
                
                axes.append(ax)

            self.add_time_to_title(snap_indices[0])
            self.style_subplots()
            self.tight_layout()

            return axes, self.suptitle,

        def animate(t):
            print(f"\tMaking frame {t} of [{snap_indices[0]}-{snap_indices[-1]}]")
            for ax in self.axs1d:
                if not ax.assume_frozen and ax.used:
                    ax(time_slice=t, toroidal_slice=toroidal_slice, poloidal_slice=poloidal_slice, update=True)
            
            self.add_time_to_title(t)

            return axes, self.suptitle

        self.animation = animation.FuncAnimation(self.fig, animate, frames=snap_indices, blit=False, init_func=init_animation, repeat = True, interval = 1, cache_frame_data=False)

    def animate_on_repeat(self):
        print("Animating on repeat: close figure to finish")
        plt.show()
        print("Done")
    
    def save_animation(self, filename):
        usrenv = UserEnvironment()

        writer = animation.FFMpegWriter(fps=usrenv.animation_framerate,
                                        metadata=dict(artist=usrenv.author_name),
                                        bitrate=usrenv.animation_bitrate,
                                        codec=usrenv.animation_codec)
        
        animation_filename = filename.with_suffix('.'+usrenv.animation_format)

        print(f"Saving video as {animation_filename}")
        self.animation.save(animation_filename, writer=writer, dpi=usrenv.animation_dpi)
        print("Done")