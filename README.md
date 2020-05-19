# GRILLIX Analysis in Python

A set of scripts to simplify post-processing of GRILLIX simulations.

Highlights:
*  Unit handling with the `pint` library
*  Calculation of normalisation quantities from a `physical_parameters.nml` file
*  Equilibrium definitions, allowing built-in field-line tracing and vector-projections
*  Fortran-namelist readers to interface with parameter files
*  Optimised routine for forward and reverse conversion of unstructured vector (x,y,z) to matrix z(x,y)
*  Automatic annotation of divertor, seperatrix, and penalisation characteristics
*  Animation and plotting routines which can be run directly on supercomputers (requires `anaconda/3` and `ffmpeg` modules)

# Setting up environment
The analysis routines require several external python libraries to be installed before use. To install packages
without `sudo` access we can use "virtual environments", which are essentially copies of Python over which
you have complete control.

First, load the most recent versions of Python3 and Anaconda3 that are available.

Then, make a hidden folder with `mkdir ~/.virtualenvs`

There are two options for virtual environments -- either, you can tell Python to use packages which are
already installed on the system, or ignore everything and start from scratch. There are advantages to 
each -- you can choose, or make both and switch between them

## Virtual environment (clean install)
Make a new virtual environment called `fci` (the name `fci` doesn't matter, but we will refer 
to it as such from hereon)
`python -m venv ~/.virtualenvs/fci`

Run `source ~/.virtualenvs/fci/bin/activate` to activate the Python virtual environment. 
You can check that you've done this correctly via `which python`. If it 
returns `~/.virtualenvs/fci/bin/python` then everything is working correctly.

Install the local packages. These will change over time, and as a general rule whenever
you need a new package then add it to this list. Most examples should work with

```
pip install --upgrade pip
pip install wheel
pip install numpy scipy matplotlib pandas vext.pyqt5 seaborn ipdb
pip install netCDF4 f90nml pint
```

Everytime you want to use the environment, run `source ~/.virtualenvs/fci/bin/activate`, and to exit (i.e. recover the system
Python installation) run `deactivate`. If you use the routines frequently, you can add them to your startup script (i.e. `.bashrc`).
N.b. if you don't use `bash`, you might need one of the other `activate` scripts in `~/.virtualenvs/fci/bin/`.

## Virtual environment using system packages
The installation method is much the same as above. We make a new virtual environment -- this one
we call `fci_sys` -- via `python -m venv ~/.virtualenvs/fci_sys --system-site-packages` where 
`--system-site-packages` means use the packages that the system `pip` installed.

Then `source ~/.virtualenvs/fci_sys/bin/activate` and
```
pip install --upgrade pip
pip install wheel
pip install --upgrade scipy matplotlib numpy
pip install netCDF4 f90nml pint ipdb seaborn
```
which requests the lastest version of `scipy`, `numpy` and `matplotlib`. This method often works better, since it uses
the built-in `PyQt5`.

## User environment
There are several settings which you may wish to tune, but typically want to keep constant once you find
working values. These are stored in `user_environment.json`. An example is given below
```
{
    "user_name": "tbody",
    "default_run_directory": "/ptmp/tbody/GRILLIX_runs/",
    "screen_dimension_x": 1920,
    "screen_dimension_y": 1200,
    "default_figure_size_x": 800,
    "default_figure_size_y": 600,
    "default_figure_resolution": 100,
    "author_name": "thomasbody",
    "animation_framerate": 10,
    "animation_bitrate": -1,
    "animation_format": "avi",
    "animation_dpi": 150,
    "animation_codec": "h264",
    "max_vector_points_per_dim": 1000,
    "vector_scale_factor": 8
}
```
The only line which must be included is `default_run_directory`, which helps to resolve filepaths
which are given relative to the default run directory rather than the script location. See `interface/UserEnvironment.py` for
information on the variables (including default values).

## Extras
At this point, you're ready to run the analysis routines. You can also choose to install
`pip install fortran-language-server` which can work with IDEs to debug your Fortran
code.

You can also add the `grillix_analysis` directory to your `PATH` via `export PATH="${PATH}:/path/to/grillix_analysis` and
`export PYTHONPATH="${PYTHONPATH}:/path/to/grillix_analysis`. This allows you to run scripts like
`poloidal_plot.py <command_line_args>`
instead of
`python path/to/grillix_analysis/poloidal_plot.py <command_line_args`

If this doesn't work, you might need to add a shebang `#!/usr/bin/env python` and run
`chmod +x <script_name>` to make your script executable.

# Developer guide

There are two sorts of scripts in the repository -- "top-level" scripts which stored at the repository level, and "source"
scripts which are stored in `source`. Generally speaking, top-level scripts should have a simple user interface and minimal
code, while source scripts are packages or classes which can be used by top-level scripts.

A top-level script will have the structure

```python
# Read the command line arguments
CLI = CommandLineInterface(...)

# Set up the "Run" superobject
run = Run(CLI["filepath"])

# Select which variables to plot
from source.Variable import variable_groups
variables = variable_groups[CLI["group"]]

# Select a projector to convert (x,y,z) vectors to z(x,y) matrices
projector = Projector(...)

# Make a Display object to plot the result
figure = Display(...) #Typically Plot(...) or Animate(...)

# Set what data should be displayed (i.e. pointers to data)
figure.set_data_array(...)

# Actually fill the values
figure.fill_values(...)

# Save or display the figure
if CLI["save"]:
    figure.save(...)
else:
    figure.show()
```



