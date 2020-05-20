from source import plt, np

def find_contour_levels(x_values, y_values, shaped_data, levels):

    cs = plt.contour(x_values, y_values, shaped_data, levels=levels)

    contour_levels = np.empty((len(levels)), dtype=ContourLevel)

    for contour_set, level_index in zip(cs.collections, range(len(levels))):
        x_segments = []
        y_segments = []
        for segment in contour_set.get_paths():
            x_segments.append(np.array(segment.vertices[:, 0]))
            y_segments.append(np.array(segment.vertices[:, 1]))
        contour_levels[level_index] = ContourLevel(x_segments, y_segments)

    plt.close()
    return contour_levels

class ContourLevel():

    def __init__(self, x_arrays, y_arrays):

        self.x_arrays = x_arrays
        self.y_arrays = y_arrays
        assert(len(x_arrays)==len(y_arrays))
        self.n_arrays = len(x_arrays)
    
    from source.shared.properties import (update_run_values, run, convert)
    
    def update_normalisation_factor(self):
        self.R0 = self.normalisation.R0

    def plot(self, ax, **kwargs):

        if self.convert:
            # Plot with units
            normalisation = self.R0
        else:
            normalisation = 1.0
        
        for x_array, y_array in zip(self.x_arrays, self.y_arrays):
                ax.plot(x_array*normalisation, y_array*normalisation, **kwargs)
