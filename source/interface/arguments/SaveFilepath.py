from pathlib import Path
from . import CLIArgument

flag_file = Path(__file__).absolute().parents[3] / "no.interactive"

class SaveFilepath(CLIArgument):
    def __init__(self, CLI):
        super().__init__(CLI, "save")
        self.parser.add_argument("-s", "--save",
            default="", type=str,
            help="Directory to save result. Leave blank to not save."
        )
    
    def __call__(self):
        if not(self.value):
            print(f"Will not save")
            assert(not(flag_file.exists())), f"Requested non-interactive backend but did not request to save. Remove {flag_file} to allow interactive plotting"
            return False
        else:
            save_filepath = self.CLI.output_path/self.value
            if save_filepath.suffix:
                raise AssertionError(f"Path should not be given with extension (was {save_filepath.suffix})")
            
            print(f"Will save into {save_filepath.parent} as '{save_filepath.name}'")
            if not(save_filepath.parent.exists()):
                raise AssertionError(f"Error: save directory '{save_filepath.parent}' does not exist")
            if not(save_filepath.parent.is_dir()):
                raise AssertionError(f"Error: save directory '{save_filepath.parent}' is not a directory")
            if save_filepath.is_dir():
                raise AssertionError(f"Error: file '{save_filepath.name}' is a directory")
            
            for extension in self.CLI.valid_extensions:
                if (save_filepath.with_suffix(extension)).exists():
                    print(f"Warning: file {save_filepath.with_suffix(extension)} exists, may overwrite.")
            
            return save_filepath