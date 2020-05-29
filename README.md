# GRILLIX Analysis in Python

A set of scripts to simplify post-processing of GRILLIX simulations.

**Highlights**

*  Unit handling with the `pint` library
*  Calculation of normalisation quantities from a `physical_parameters.nml` file
*  Equilibrium definitions, allowing built-in field-line tracing and vector-projections
*  Fortran-namelist readers to interface with parameter files
*  Optimised routine for forward and reverse conversion of unstructured vector (x,y,z) to matrix z(x,y)
*  Automatic annotation of divertor, seperatrix, and penalisation characteristics
*  Animation and plotting routines which can be run directly on supercomputers (requires `anaconda/3` and `ffmpeg` modules)

**Contents**
- [GRILLIX Analysis in Python](#grillix-analysis-in-python)
- [Top-level scripts](#top-level-scripts)
- [Setting up environment](#setting-up-environment)
  - [Virtual environment (clean install)](#virtual-environment-clean-install)
  - [Virtual environment using system packages](#virtual-environment-using-system-packages)
  - [When things go wrong](#when-things-go-wrong)
  - [User environment](#user-environment)
- [Extras](#extras)
- [Known issues](#known-issues)

# Top-level scripts

There are three sorts of scripts in the repository -- "top-level" scripts which stored at the repository level, "source" scripts which are stored in `source`, and "tools" which are stored in `tools`. Generally speaking, top-level scripts should have a simple user interface and minimal code, while source scripts are packages or classes which can be used by top-level scripts. Tools need the module virtual environment, but otherwise are completely independent from the rest of the module, and simplify common tasks.

Each top level script has a command-line interface. You can see this interface by adding `--help` to the argument list.

**Scripts available**

  * `poloidal_plot.py`: plot values over a poloidal plane
  * `poloidal_animate.py`: animate values over a poloidal plane
  * `normalisation.py`: return the normalisation values calculated from `physical_parameters.nml`
  * `tools/set_interactive.py`: makes or deletes a file `no.interactive` which forces the use of the non-interactive `Agg` backend (useful if running on a server which doesn't have a DISPLAY)
  * `tools/snap_length.py`: returns the number of snaps and last tau value of a directory
  * `tools/crop_snaps.py`: backs up the current snaps and then makes snaps over a specified snap range. (Warning: if this script crashes halfway it can result in unusable snaps with no backup).

**Interface for top-level scripts**

The command-line arguments are defined in `source/interface/arguments`.

The only required argument is `--filepath`, which specifies which directory the analysis should be run on. You can either give the path relative to the current working directory, or relative to the `default_run_directory` (see user environment section). To run in the current working directory, use `--filepath=.`

The optional arguments are
  * `--group`: which measurement_group to display. See `source/measurements/measurement_groups.py` or `--help` for available options. The figure will automatically generate subplots for each variable. Feel free to add new variable groups.
  * `--save`: filename to save the result as. Will be saved into `output`, unless a full filepath is given.
  * `--title`: title of the plot (otherwise the parent directory and run directory will be used)
  * `--time_slice`: which snaps to display/calculate over. Given as a Python `slice`: so interpreted as `start, stop, step`. See implementation for more details
  * `--toroidal_slice`: which planes to calculate over. Leave blank to access all planes. N.b. some operators such as parallel gradient require all snaps to be loaded.
  * `--reduction`: function to remove extra dimensions (i.e. `mean` which will take the average over planes and/or time)

Optional flags are
  * `--SI_units`: plot the values in SI units
  * `--exclude_outliers`: exclude values outside the quartile range specified in `user_environment.json`
  * `--log_scale`: use a logarithmic (or symmetric-logarithmic) scale
  * `--error_snaps`: display the values from error_snaps instead of snaps


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
the built-in `PyQt5`. Sometimes you will want to get a version of a package, even though it is already installed on the system. In this case, you can add a `--ignore-installed` flag to `pip` and it will download and install its own version.

## When things go wrong
Unfortunately, sometimes there can be issues with the python packages. If this is the case, try the following steps

  0. Make sure you've activated the environment (i.e. `source ~/.virtualenvs/...`)
  1. Starting simple, if you're getting a "module not found" error, try `pip --install <module name>` or `pip --upgrade <module name>`
  2. If you get errors about missing/extra arguments to a library function, check the signature online. If it matches the code, then update your version of the module. If it doesn't match the code, fix the code to match the updated signature (and update your module for good measure).
  3. If it all goes terribly wrong: remove your virtual environment folder `rm -rf ~/.virtualenv/fci(_sys)` and start again. The good thing about virtual environments is that they are entirely local. If you're having problems, you can `deactivate` one and make another, and test them in parallel.

## User environment
There are several settings which you may wish to tune, but typically want to keep constant once you find working values. These should be stored in `user_environment.json`. Most values have defaults set in `source/interface/UserEnvironment.py` -- a minimal file would look like
```
{
    "user_name": "your username on the current system",
    "default_run_directory": "full path to where you store your runs",
    "author_name": "your name for adding to metadata",
}
```
The only line which must be included is `default_run_directory`, which helps to resolve filepaths
which are given relative to the default run directory rather than the script location.

# Extras
At this point, you're ready to run the analysis routines. You can also choose to install
`pip install fortran-language-server` which can work with IDEs to debug your Fortran
code.

You can also add the `grillix_analysis` directory and the `tools` subdirectory to your `PATH` via 
```
export PATH="${PATH}:/path/to/grillix_analysis:/path/to/grillix_analysis/tools
export PYTHONPATH="${PYTHONPATH}:/path/to/grillix_analysis:/path/to/grillix_analysis/tools
```
This allows you to run scripts like
`poloidal_plot.py <command_line_args>`
instead of
`python path/to/grillix_analysis/poloidal_plot.py <command_line_args`

If this doesn't work, you might need to add a shebang `#!/usr/bin/env python` and run
`chmod +x <script_name>` to make your script executable.

# Known issues
**1. Bus error: animating a run which has snaps being written to it**

This is essentially a stack-overflow, raised when trying to access non-accessible memory. The scripts open each NetCDF file _once_ at the start to reduce overhead from opening and closing files. This can cause an error if the NetCDF files are currently being written (i.e. by GRILLIX). If you encounter this issue, the best solution is to copy the run to another folder and run the scripts from that folder.

**2. matplotlib.animation:MovieWriter stderr**

Particularly for long animations, it is possible that the `FFMpegFileWriter` crashes when trying to stitch together the `_tmp*.png` files into an animation. Usually this will return with an error like 
```
CalledProcessError(-7, ['ffmpeg', '-r', '15', '-i', '_tmp%07d.png', '-vframes', '<number of PNG files>', '-vcodec', 'h264', '-pix_fmt', 'yuv420p', '-b', '7500k', '-y', <output filepath>], ...)
```
This is actually a shell command, corresponding to `'ffmpeg -r 15 -i _tmp%07d.png -vframes <number of PNG files> -vcodec h264 -pix_fmt yuv420p -b 7500k -y' <output filepath>`. Usually you can recover from the error by executing the sheel command directly and then removing the temporary PNG files.

You might have to change `-b` to `-b:v` (seems that the Python call to FFMpeg has a slight error with the interface).

