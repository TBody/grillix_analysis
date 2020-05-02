from source.Run import Run

run = Run('TCV_half/init_start')

from source.Display import Plot

figure = Plot(ncols=4, SI_conversion=True)

from source.Projector.Poloidal import Poloidal
from source.Variable import Density, ParallelVelocity, AlfvenSpeed, DynamicalPlasmaBeta
from source.Operator import Operator

projector = Poloidal

figure.axs[0,0].set_data(run=run, projector=projector, variable=Density)
figure.axs[1,0].set_data(run=run, projector=projector, variable=ParallelVelocity)
figure.axs[2,0].set_data(run=run, projector=projector, variable=AlfvenSpeed)
figure.axs[3,0].set_data(run=run, projector=projector, variable=DynamicalPlasmaBeta)

figure.axs[0,0](toroidal_slice=0)
figure.axs[1,0](toroidal_slice=0)
figure.axs[2,0](toroidal_slice=0)
figure.axs[3,0](toroidal_slice=0)

figure.show()