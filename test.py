from ipdb import launch_ipdb_on_exception
from source import plt, np
from source.shared.common_functions import smoothstep


with launch_ipdb_on_exception():
    from source.Run import Run

    run = Run('TCV_half/init_start')

    from source.Display import Plot

    # figure = Plot(run=run, ncols=4, nrows=1, convert=True)

    from source.Projector.Poloidal import Poloidal
    from source.Operator import AllReduction
    from source.Variable import (PhiForward, PhiBackward, PhiBetweenTargets)
    from source.Operator import AllReduction

    # variables = [PhiForward, PhiBackward, PhiBetweenTargets]

    projector = Poloidal(reduction=AllReduction(), run=run)

    # figure.set_data_array(run=run, projector=projector, variables=variables, operators=[])

    # figure.fill_values()

    # figure.show()


    chi_width = 5
    npol = 16
    step_order = 3
    step_width = chi_width*2*np.pi/npol

    phi_forward = projector(PhiForward(run=run))
    phi_backward = projector(PhiBackward(run=run))

    pen_chi = 1.0 + smoothstep(0.0, phi_backward, step_width, step_order) - smoothstep(0.0, phi_forward, step_width, step_order)

    backtrace = projector.structure_z(smoothstep(2*step_width, phi_backward, step_width, step_order))
    forwtrace = projector.structure_z(smoothstep(-2*step_width, phi_forward, step_width, step_order))

    structured_chi = projector.structure_z(pen_chi)
    from source.shared.ContourLevel import find_contour_levels
    contours = find_contour_levels(projector.x, projector.y, structured_chi, [0, 0.5, 1 - np.finfo('float').eps])

    backcont = find_contour_levels(projector.x, projector.y, backtrace, [0.5])
    forwcont = find_contour_levels(projector.x, projector.y, forwtrace, [0.5])

    fig, axs = plt.subplots(ncols = 3, sharex=True, sharey=True)
    axs[0].pcolormesh(projector.x, projector.y, structured_chi)
    axs[1].pcolormesh(projector.x, projector.y, backtrace)
    axs[2].pcolormesh(projector.x, projector.y, forwtrace)

    for i in range(3):
        contours[0].plot(axs[i], color='r')
        contours[1].plot(axs[i], color='r')
        contours[2].plot(axs[i], color='r')
        
        forwcont[0].plot(axs[i], color='b')
        backcont[0].plot(axs[i], color='b')

        axs[i].set_aspect('equal')

    plt.show()
