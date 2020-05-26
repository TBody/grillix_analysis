from source import np, perceptually_uniform_cmap, diverging_cmap, mplcolors

def find_static_colormap_normalisation(self, **kwargs):
    # Find colormap normalisation over a range, without plotting.
    # Useful for animating since it ensures that no points are clipped from the colormap
    values, _ = self.measurement(**kwargs)
    
    self.find_colormap_normalisation(values=values)

def find_colormap_normalisation(self, values):

    [cbar_min, cbar_max] = self.data_limits(values)
    maximum_magnitude = np.max([np.abs(cbar_min), np.abs(cbar_max)])

    if not self.log_scale:
        # Linear (standard) colormap
        if cbar_min >= 0 or not(self.measurement.variable.allow_diverging_cmap):
            self.colormap_norm = mplcolors.Normalize(vmin=cbar_min, vmax=cbar_max)
            self.colormap = perceptually_uniform_cmap
        else:
            self.colormap_norm = mplcolors.Normalize(vmin=-maximum_magnitude, vmax=maximum_magnitude)
            self.colormap = diverging_cmap
    
    elif cbar_min > 0:
        # Standard log colormap
        self.colormap_norm = mplcolors.LogNorm(vmin=cbar_min, vmax=cbar_max)
        self.colormap = perceptually_uniform_cmap

    else:
        # Symlog colormap
        # Ignore values which are exactly zero
        abs_sort = np.sort(np.abs(values.ravel()))

        # Increase the linear_proportion with the zero values
        linthres = np.nanquantile(np.abs(values.ravel()), self.linear_proportion)
        zero_proportion = 1 - np.count_nonzero(abs_sort)/len(abs_sort)
        self.linear_proportion += zero_proportion

        linscale = ((np.log10(cbar_max) - np.log10(linthres)) + (np.log10(-cbar_min) - np.log10(linthres)))*self.linear_proportion

        if cbar_max <= 0:
            # All negative values
            self.colormap_norm = mplcolors.SymLogNorm(linthresh=0, linscale=linscale,
                                                vmin=cbar_min, vmax=cbar_max, base=10)
            self.colormap = perceptually_uniform_cmap
        elif self.measurement.variable.allow_diverging_cmap:
            # Diverging about zero
            self.colormap_norm = mplcolors.SymLogNorm(linthresh=linthres, linscale=linscale,
                                                vmin=-maximum_magnitude, vmax=maximum_magnitude, base=10)
            self.colormap = diverging_cmap
        else:
            # Non-centred
            self.colormap_norm = mplcolors.SymLogNorm(linthresh=linthres, linscale=linscale,
                                                vmin=cbar_min, vmax=cbar_max, base=10)
            self.colormap = diverging_cmap

    self._colormap_calculated = True

def data_limits(self, values):

    if self.exclude_outliers:
        return np.nanquantile(values.ravel(), self.outliers_quantitles)
    else:
        return np.nanmin(values), np.nanmax(values)