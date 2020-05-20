from ipdb import launch_ipdb_on_exception
from source.canvas.layout import Figure, Axes
from source import plt

with launch_ipdb_on_exception():
    from source.run import Run

    fig = Figure()

    fig.add_subplots(nrows=2, ncols=2)

    fig.make_suptitle("Test")

    fig.show()