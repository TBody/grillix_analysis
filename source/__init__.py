# Import modules which are globally required
from source.interface import UserEnvironment
usrenv = UserEnvironment()

# Base system requirements
import os
import sys
import time
import warnings

# Filepaths
from pathlib import Path
# NetCDF file interface
from netCDF4 import Dataset

# Numerical analysis
import numpy as np
import numpy.ma as ma
# Datasets
import pandas as pd

# Plotting
import matplotlib
flag_file = Path(__file__).absolute().parents[1] / "no.interactive"
print(f"Flag file {flag_file} does{'' if flag_file.exists() else ' not'} exist. Setting backend {usrenv.noninteractive_backend if flag_file.exists() else usrenv.interactive_backend}")
if flag_file.exists():
    matplotlib.use(usrenv.noninteractive_backend)
else:
    matplotlib.use(usrenv.interactive_backend)
# Interactive figures
import matplotlib.pyplot as plt
mplstyle = (Path(__file__).absolute().parent / "canvas" / usrenv.matplotlib_style).with_suffix(".mplstyle")
plt.style.use(mplstyle)
import matplotlib.colors as mplcolors
# Pretty plotting
import seaborn as sns

perceptually_uniform_cmap = plt.get_cmap('inferno')
diverging_cmap = plt.get_cmap('RdBu_r')

# Dictionaries which return [] for no-value
from collections import defaultdict

# Units
# Disable Pint's old fallback behavior (must come before importing Pint)
os.environ['PINT_ARRAY_PROTOCOL_FALLBACK'] = "0"
# See Shared/unit_registry.txt for defined units
import pint
unit_registry = pint.UnitRegistry()
Quantity = unit_registry.Quantity
Dimensionless = Quantity(1, "")

# Silence NEP 18 warning
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    Quantity([])

unit_registry.setup_matplotlib()
unit_registry.default_format = '~'

import source.shared.pint_extension

from .Component import Component