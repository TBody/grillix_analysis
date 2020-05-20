
class RunComponent:

    def __init__(self, run):
        self.run = run
    
    @property
    def run(self):
        return self._run

    @run.setter
    def run(self, value):
        if value != None:
            self._run = value
    
    @property
    def SI_units(self):
        return self.run.SI_units
    
    @property
    def normalisation(self):
        return self.run.normalisation

from .NamelistReader import NamelistReader
from .NetCDFPath import NetCDFPath
from .Polygon import Polygon
from .ContourLevel import ContourLevel, find_contour_levels
