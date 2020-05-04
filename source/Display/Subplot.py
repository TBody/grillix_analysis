from source import np, perceptually_uniform_cmap, diverging_cmap, mplcolors, Quantity

from source.Run import Run
from source.Projector import Projector
from source.Variable import Variable
from source.Operator import Operator

from mpl_toolkits.axes_grid1 import make_axes_locatable

class Subplot():
    
    def __init__(self, display, ax, **kwargs):
        # Initialises the basic Subplot class
        self.display = display
        self.ax = ax
        self.hide_xlabel = False
        self.hide_ylabel = False
        self.assume_frozen = False

        self.cmap = None
        self.cmap_norm = None

        self.used = False
        
    @property
    def run(self):
        # print(f"self {self} called run")
        return self._run

    @run.setter
    def run(self, value):
        # print(f"self {self} called run with arg {value}")
        if value != None:
            self._run = value

    @property
    def convert(self):
        # print(f"self {self} called convert")
        return self.display.convert

    @convert.setter
    def convert(self, value):
        # print(f"self {self} called convert with arg {value}")
        raise NotImplementedError(f"Should set convert directly on display")   
        
    @property
    def display_logarithmic(self):
        # print(f"self {self} called display_logarithmic")
        return self.display.display_logarithmic

    @display_logarithmic.setter
    def display_logarithmic(self, value):
        # print(f"self {self} called display_logarithmic with arg {value}")
        raise NotImplementedError(f"Should set display_logarithmic directly on display")   

    def set_data(self, run, projector, variable, operators=[]):
        # Must pass an initialised Run object
        # Can pass uninitialised projector, variable and operators -- in this case __init__(run) is called
        
        self.run = run
        self.run.convert = self.convert
        
        # If type(object) == type, call __init__ (will set run values later anyway)
        if type(projector) == type:
            projector = projector()
        if type(variable) == type:
            variable = variable()

        operators = [operator() if type(operator) == type else operator for operator in operators]
        
        self.projector = projector
        self.variable = variable
        # If the list of operators is of length 1, expand to be a 1D array
        self.operators = np.atleast_1d(np.array(operators, dtype=Operator))

        # Check that the data types are correct, since this can be tricky to get correct (recommend using kwargs)
        assert(isinstance(run, Run))
        assert(isinstance(projector, Projector))
        assert(isinstance(self.variable, Variable))
        for operator in self.operators:
            assert(isinstance(operator, Operator))
        
        self.projector.run = self.run
        self.variable.run = self.run
        for operator in self.operators:
            operator.run = self.run
        
        self.used = True

    def find_z_values(self, **kwargs):
        # Can supply slices as keyword arguments. Must match the projector slice names

        z = self.projector(self.variable, **kwargs)
        
        for operator in self.operators:
            z = operator(z)
        
        z = self.projector.structure_z(z)

        return np.squeeze(z)

    def __call__(self, update=False, **kwargs):

        self.z = self.find_z_values(**kwargs)
        
        if not update:
            # First plot
            if self.variable.numerical_variable:

                if self.cmap == None or self.cmap_norm == None:
                    self.find_colormap_limits_from_z(self.z)
                
                self.plot = self.ax.pcolormesh(self.projector.x, self.projector.y, self.z, cmap=self.cmap, norm=self.cmap_norm)

            else:
                self.plot = self.ax.pcolormesh(self.projector.x, self.projector.y, self.z)
            
            # create an axes on the right side of ax. The width of cax will be 5%
            # of ax and the padding between cax and ax will be fixed at 0.05 inch.
            divider = make_axes_locatable(self.ax)
            cax = divider.append_axes("right", size="5%", pad=0.05)
            self.cbar = self.display.fig.colorbar(self.plot, cax=cax)

            self.ax.format_coord = self.format_coord

            self.projector.annotate(self)
        else:
            pass
    
    def format_coord(self, x, y):

        if ((x > self.projector.x.min()) & (x <= self.projector.x.max()) &
            (y > self.projector.y.min()) & (y <= self.projector.y.max())):
            row = np.searchsorted(self.projector.x, x)-1
            col = np.searchsorted(self.projector.y, y)-1
            z = self.z[col, row]
            
            # See if the field defines a custom formatter for z values. If not, just print the value
            format_value = getattr(self.variable, "__format_value__", None)
            if callable(format_value):
                return f'x={x:f}, y={y:f}, z={format_value(z)}   [{row},{col}]'
            else:
                return f'x={x:f}, y={y:f}, z={z:f}   [{row},{col}]'
            
        else:
            return 'x={:f}, y={:f}'.format(x, y)
    
    def style_plot(self, **kwargs):
        if self.used:
            self.ax.set_aspect('equal')
            self.projector.annotate.style_plot(self)
            if self.convert:
                self.ax.set_title(f"{self.variable.title} [{self.variable.normalisation_factor.units}]")
            else:
                self.ax.set_title(self.variable.title)
        else:
            self.ax.clear()
            self.ax.set_axis_off()
            self.ax.set_frame_on(False)
    
    def find_colormap_limits(self, quantiles=(0.001, 0.999), linear_proportion=0.20, **kwargs):
        # Useful to precompute (non-changing) colormaps
        z = self.find_z_values(**kwargs)
        self.find_colormap_limits_from_z(z, quantiles)

    def find_colormap_limits_from_z(self, z, quantiles=(0.001, 0.999), linear_proportion=0.20):
        # For use with
        #   colors.SymLogNorm(linthresh=linthres, linscale=linscale, vmin=vmin, vmax=vmax, base=10) for vmin <= 0
        #   norm=colors.LogNorm(vmin=vmin, vmax=vmax) for vmin > 0
        
        assert(len(quantiles)==2)
        [self.vmin, self.vmax] = self.find_quantile_limits_from_z(z, quantiles)
        
        if self.vmin > 0:
            self.linthres = 0
            self.linscale = 0
        else:
            # Ignore values which are exactly zero
            abs_sort = np.sort(np.abs(z.ravel()))
            
            # Increase the linear_proportion with the zero values
            self.linthres = self.find_absquantile_limits_from_z(abs_sort[abs_sort!=0], linear_proportion)
            zero_proportion = 1 - np.count_nonzero(abs_sort)/len(abs_sort)
            linear_proportion += zero_proportion
            
            self.linscale = ((np.log10(self.vmax) - np.log10(self.linthres)) + (np.log10(-self.vmin) - np.log10(self.linthres)))*linear_proportion
        
    def find_quantile_limits_from_z(self, z, quantiles):
        try:
            return np.nanquantile(z.ravel(), quantiles)
        except TypeError:
            return np.nanquantile(z.magnitude.ravel(), quantiles)
    
    def find_absquantile_limits_from_z(self, z, quantiles):
        try:
            return np.nanquantile(np.abs(z.ravel()), quantiles)
        except TypeError:
            return np.nanquantile(np.abs(z.magnitude.ravel()), quantiles)
    
    def find_colormap(self, z=None, quantiles=(0.001, 0.999), linear_proportion=0.20, **kwargs):
        if z == None:
            z = self.find_z_values(**kwargs)
        
        self.find_colormap_limits_from_z(z, quantiles=quantiles, linear_proportion=linear_proportion)

        if not self.display_logarithmic:
            self.cmap_norm = mplcolors.Normalize(vmin=self.vmin, vmax=self.vmax)
            if self.vmin > 0:
                self.cmap = perceptually_uniform_cmap
            else:
                self.cmap = diverging_cmap

        elif self.vmin > 0:
            self.cmap_norm = mplcolors.LogNorm(vmin=self.vmin, vmax=self.vmax)
            self.cmap = perceptually_uniform_cmap
        elif self.vmax <= 0:
            self.cmap_norm = mplcolors.SymLogNorm(linthresh=self.linthres, linscale=self.linscale,
                                                vmin=self.vmin, vmax=self.vmax, base=10)
            self.cmap = perceptually_uniform_cmap
        else:
            maximum_magnitude = np.max([np.abs(self.vmin), np.abs(self.vmax)])
            self.cmap_norm = mplcolors.SymLogNorm(linthresh=self.linthres, linscale=self.linscale,
                                                vmin=-maximum_magnitude, vmax=maximum_magnitude, base=10)
            self.cmap = diverging_cmap
