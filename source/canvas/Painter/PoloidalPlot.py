from source import matplotlib
from . import Painter
from ._artists import pcolormesh, quiver

class PoloidalPlot(Painter):
    
    def __init__(self, *args, colorbar=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.colorbar = colorbar
    
    @property
    def colorbar(self):
        if self._colorbar is None:
            raise RuntimeError(f"Colorbar has not yet been set")
        else:
            return self._colorbar
    
    @colorbar.setter
    def colorbar(self, value):
        self._colorbar = value
        if self._colorbar is not None:
            self._colorbar._painter = self

    def draw_plot(self):

        if self._values.is_vector:
            self.artist = quiver(self, self.colorbar)
        else:
            self.artist = pcolormesh(self, self.colorbar)
        
        self.annotate_plot()
        self.style_plot()

    def plot_in_SI(self, x, y, **kwargs):
        lines, = self.ax.plot(x * self.x_normalisation.magnitude, y * self.y_normalisation.magnitude, **kwargs)
        return lines

    def annotate_plot(self):
        default_linewidth = matplotlib.rcParams['lines.linewidth']

        for annotation_plot in [
            self.plot_in_SI(self.run.divertor_polygon.x_points, self.run.divertor_polygon.y_points, color='b', linewidth=default_linewidth*0.5),
            self.plot_in_SI(self.run.exclusion_polygon.x_points, self.run.exclusion_polygon.y_points, color='r', linewidth=default_linewidth*0.5),
            self.run.seperatrix[0].plot_all_arrays(plot_function=self.plot_in_SI, color='g', linewidth=default_linewidth*0.5),
            self.run.penalisation_contours[0].plot_all_arrays(plot_function=self.plot_in_SI, color='r', linestyle='--', linewidth=default_linewidth*0.5),
            self.run.penalisation_contours[-1].plot_all_arrays(plot_function=self.plot_in_SI, color='r', linestyle='--', linewidth=default_linewidth*0.5),
            self.run.parallel_limit_contours[0].plot_all_arrays(plot_function=self.plot_in_SI, color='b', linestyle='--', linewidth=default_linewidth*0.5),
            self.run.parallel_limit_contours[1].plot_all_arrays(plot_function=self.plot_in_SI, color='b', linestyle='--', linewidth=default_linewidth*0.5)
        ]:
            if type(annotation_plot) is list:
                self.annotations += annotation_plot
            else:
                self.annotations.append(annotation_plot)

    def style_plot(self):
        self.ax.format_coord = self.format_coord
        self.ax.set_aspect('equal')

        self.ax.set_xlim(self.projector.xmin * self.x_normalisation.magnitude, self.projector.xmax * self.x_normalisation.magnitude)
        self.ax.set_ylim(self.projector.ymin * self.y_normalisation.magnitude, self.projector.ymax * self.y_normalisation.magnitude)

        if self.SI_units:
            self.title = self.ax.set_title(f"{self.measurement.title_string()} [{self.units.units}]")
        else:
            self.title = self.ax.set_title(self.measurement.title_string())
    
    