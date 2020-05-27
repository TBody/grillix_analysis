from source import usrenv, np

class Artist:

    def __init__(self):
        pass

    def set_blank_data(self):
        pass
    
    def __getattr__(self, key):
        try:
            return getattr(self.artist, key)
        except AttributeError:
            raise AttributeError(f"{self.__class__.__name__} has no attribute {key}")

class pcolormesh(Artist):

    def __init__(self, painter, colorbar):
        self.painter = painter
        self.colorbar = colorbar
        
        self.artist = painter.ax.pcolormesh(
            painter.x_values.magnitude,
            painter.y_values.magnitude,
            painter.values,
            cmap=colorbar.colormap,
            norm=colorbar.colormap_norm
            )
    
    def update_values(self):
        self.artist.set_array(self.painter.values[:-1, :-1].ravel())

class quiver(Artist):

    def __init__(self, painter, colorbar):
        self.painter = painter
        self.colorbar = colorbar

        max_vector_points = usrenv.max_vector_points_per_dim
        vector_scale_factor = usrenv.vector_scale_factor

        x_samples = np.unique(np.floor(np.linspace(0, 1, num=max_vector_points)*(painter.projector.x.size-1))).astype(int)
        y_samples = np.unique(np.floor(np.linspace(0, 1, num=max_vector_points)*(painter.projector.y.size-1))).astype(int)

        vector_magnitude = painter.values.vector_magnitude[y_samples,:][:, x_samples]
        
        vector_scale_factor = max_vector_points*np.nanmax(vector_magnitude)/vector_scale_factor

        self.artist = painter.ax.quiver(
            painter.x_values.magnitude[x_samples],
            painter.y_values.magnitude[y_samples],
            painter.values.R[y_samples,:][:, x_samples],
            painter.values.Z[y_samples,:][:, x_samples],
            vector_magnitude,
            cmap=colorbar.colormap,
            norm=colorbar.colormap_norm,
            pivot='mid',
            angles='xy',
            linewidth=1,
            scale=vector_scale_factor,
            scale_units='xy'
            )

class streamplot(Artist):

    pass