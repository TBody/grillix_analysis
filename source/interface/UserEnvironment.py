from pathlib import Path
import json

class UserEnvironment:

    def __init__(self):
        user_environment_json = Path(__file__).absolute().parents[2] / "user_environment.json"

        # Defaults
        self.user_name = None
        self.default_run_directory = None
        self.author_name = None

        # Set the plotting backend
        # Recommend using Qt5Agg for interactive plots, or Agg for non-interactive plots
        self.plot_backend = "Qt5Agg"
        self.matplotlib_style = "default"

        # How much space (in fractions of figure height) to leave for making the suptitle
        self.suptitle_spacing = 0.05

        # What stride to use when calculating constant colormaps?
        self.sparse_time_slice = 10
        # Animation variables
        self.animation_writer = "FFMpegFileWriter"
        self.animation_framerate = 15
        self.animation_bitrate = 7500
        self.animation_dpi = 200
        self.animation_format = "mp4"
        self.animation_codec = "h264"

        # If using exclude outliers, how much of the range to clip
        self.exclude_outliers_quantiles = (0.001, 0.999)

        # Variables for quiver (vector) plots
        self.max_vector_points_per_dim = 100
        # How much to increase/decrease the (autoscaled) vector scale factor
        self.vector_scale_factor = 1

        assert(user_environment_json.exists()), f"user_environment.json not found at {user_environment_json}"
        
        with open(user_environment_json, 'r') as usrenv:
            user_environment = json.load(usrenv)
    
        for key, value in user_environment.items():
            setattr(self, key, value)
        