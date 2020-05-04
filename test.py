from source.Run import Run

run = Run('TCV_half/init_start')

from source.Display import Plot

figure = Plot(ncols=4, nrows=2, convert=True)

from source.Projector.Poloidal import Poloidal
from source.Variable import penalisation_variables as variables
from source.Operator import Operator

projector = Poloidal

figure.set_data_array(run=run, projector=projector, variables=variables)

figure.fill_values(toroidal_slice=0)

figure.show()