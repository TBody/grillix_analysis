from ipdb import launch_ipdb_on_exception

with launch_ipdb_on_exception():
    from source.Run import Run

    run = Run('TCV_half/init_start')

    from source.Display import Plot

    figure = Plot(ncols=4, nrows=2, convert=True)
    # figure = Plot(convert=True)

    from source.Projector.Poloidal import Poloidal
    from source.Variable import magnetic_field_variables as variables
    # from source.Variable import PoloidalUnitVector
    from source.Operator import TimeReduction, ToroidalReduction

    projector = Poloidal

    operators = [TimeReduction, ToroidalReduction]

    figure.set_data_array(run=run, projector=projector, variables=variables, operators=operators)
    # figure.set_data_array(run=run, projector=projector, variables=[PoloidalUnitVector], operators=operators)

    figure.fill_values()

    figure.show()