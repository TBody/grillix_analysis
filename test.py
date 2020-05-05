from source.Run import Run

run = Run('TCV_half/init_start')

from source.Display import Plot

figure = Plot(ncols=4, nrows=2, convert=True)

from source.Projector.Poloidal import Poloidal
from source.Variable import electric_field_variables as variables
from source.Operator import TimeReduction, ToroidalReduction

projector = Poloidal

operators = [TimeReduction, ToroidalReduction]

figure.set_data_array(run=run, projector=projector, variables=variables, operators=operators)

figure.fill_values()

figure.show()