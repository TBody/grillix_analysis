from source import np, plt
from . import Display
from matplotlib import animation

class Animate(Display):
    
    def __init__(self, nrows=1, ncols=1, **kwargs):
        super().__init__(nrows=nrows, ncols=ncols, **kwargs)
    
    def animate_values(self, time_slice=slice(None), toroidal_slice=slice(None), poloidal_slice=slice(None), save=False, calculate_cbar_on_single_plane=True, cbar_time_step=1, run_directory=None, normalisation=None, convert=None):
        
        tau_values = np.atleast_1d(run_directory.snaps[0]['tau'])
        snaps_to_animate = np.arange(tau_values.size)[time_slice]
        print(f"Will animate the following snap range: {snaps_to_animate[0]} to {snaps_to_animate[-1]}")

        self.time_in_title_args = {"normalisation": normalisation, "run_directory": run_directory, "convert": convert, "tau_values": tau_values}

        cbar_time_slice = slice(time_slice.start, time_slice.step, cbar_time_step)
        # Plot the first snap in the sequence
        print("Calculating constant colormap ranges (this may take some time)")
        plots = []
        for x in range(self.ncols):
            for y in range(self.nrows):
                if not self.axs[x][y].assume_frozen:
                    plot = self.axs[x][y]
                    
                    # Read all of the data: this will take a long time for a big animation
                    if calculate_cbar_on_single_plane:
                        z = plot.data(cbar_time_slice, slice(0,1), poloidal_slice)
                    else:
                        z = plot.data(cbar_time_slice, toroidal_slice, poloidal_slice)
                    
                    # Find the colormap for the full animation
                    [cmap, lin_norm, log_norm] = plot.find_colormap(z)
                    # Draw the first plot (fixes the colormap)
                    plot.fill_values(snaps_to_animate[0], toroidal_slice, poloidal_slice, cmap, lin_norm, log_norm)

                    plots.append(plot)

        self.add_time_to_title(time_slice=snaps_to_animate[0], **self.time_in_title_args)
        
        self.style_subplots()
        self.tight_layout()

        self.read_user_environment()
                    
        Writer = animation.writers['ffmpeg']

        usrenv = {'animation_framerate': 15, "author_name": "unknown", "animation_bitrate": 1800, "animation_format": "avi"}
        for key, value in usrenv.items():
            try:
                usrenv[key] = self.usrenv[key]
            except KeyError:
                print(f"No value for {key} found in user_environment.json. Using default [{value}]")

        writer = Writer(fps=usrenv['animation_framerate'], metadata=dict(artist=usrenv['author_name']), bitrate=usrenv['animation_bitrate'])

        def init_animation():
            return plots, self.suptitle,

        def animate(t):
            print(f"\tMaking frame {t} of [{snaps_to_animate[0]}-{snaps_to_animate[-1]}]")
            for plot in plots:
                plot.update_values(t, toroidal_slice, poloidal_slice)
            self.add_time_to_title(time_slice=t, **self.time_in_title_args)

            return plots, self.suptitle


        if not(save):
            print("Animating on repeat: close figure to finish")
            anim = animation.FuncAnimation(self.fig, animate, frames=snaps_to_animate, blit=False, init_func=init_animation, repeat = True, interval = 1)
            self.show()
            print("Done")
        else:
            print(f"Saving video as {save.with_suffix('.'+usrenv['animation_format'])}")
            anim = animation.FuncAnimation(self.fig, animate, frames=snaps_to_animate, blit=False, init_func=init_animation, repeat = False, interval = 1)
            anim.save(save.with_suffix('.'+usrenv['animation_format']), writer=writer)
            print("Done")