from source import Path
import json

class UserEnvironment:

    def __init__(self):
        user_environment_json = Path(__file__).absolute().parents[2] / "user_environment.json"

        # Defaults
        self.user_name = None
        self.default_run_directory = None
        self.author_name = None
        
        self.screen_dimension_x = 1920
        self.screen_dimension_y = 1200
        self.default_figure_size_x = 1920
        self.default_figure_size_y = 1200

        self.default_figure_resolution = 100 #in dpi -- affects scaling of 'px' valued objects such as text
        
        # Animation variables
        self.animation_framerate = 15
        self.animation_bitrate = 1800
        self.animation_format = "avi"

        # Variables for quiver (vector) plots
        self.max_vector_points_per_dim = 100
        # How much to increase/decrease the (autoscaled) vector scale factor
        self.vector_scale_factor = 1

        assert(user_environment_json.exists()), f"user_environment.json not found at {user_environment_json}"
        
        with open(user_environment_json, 'r') as usrenv:
            user_environment = json.load(usrenv)
    
        for key, value in user_environment.items():
            setattr(self, key, value)
