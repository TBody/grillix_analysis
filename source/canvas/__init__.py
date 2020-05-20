from .layout import Figure, Axes

def subplots_with_title(naxs, title):
    # Makes a figure with subplots for naxs and a suptitle

    figure = Figure()
    figure.add_subplots_from_naxs(naxs=naxs)
    figure.make_suptitle(title)

    return figure
