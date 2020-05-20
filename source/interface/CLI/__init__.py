import argparse
from pathlib import Path

class BaseCLI():
    output_path = Path(__file__).absolute().parents[2]/'output'
    valid_extensions = [".png", ".svg", ".avi", ".mp4"]

    def __init__(self, description):
        self.initialised = False
        self.argument_dictionary = {}
        self.parser = argparse.ArgumentParser(description=description)

    def parse(self):
        self.args = self.parser.parse_args()
        self.initialised = True

        self.dict = {}
        for parameter in vars(self.args).keys():
            self.dict[parameter] = self.argument_dictionary[parameter]()
    
    def __str__(self):

        string = f"Script to {self.parser.description} called with parameters\n"
        for parameter, value in self.dict.items():
            string += f"\t{parameter}: {value}\n"

        return string
    
    def __getitem__(self, item):
        return self.dict[item]
    
    def __setitem__(self, key, value):
        self.dict[key] = value

from ..arguments import *