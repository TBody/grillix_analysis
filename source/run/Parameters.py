from .components import NamelistReader
from source import Path

class Parameters(NamelistReader):
    
    params_filepath_dict = {
        "grid_params_path"         : "params_grid",
        "map_params_path"          : "params_map",
        "trace_params_path"        : "params_trace",
        "init_params_path"         : "params_init",
        "tstep_params_path"        : "params_tstep",
        "physmod_params_path"      : "params_physmod",
        "bndconds_params_path"     : "params_bndconds",
        "bufferz_params_path"      : "params_bufferz",
        "srcsnk_params_path"       : "params_srcsnk",
        "floors_params_path"       : "params_floors",
        "multigrid_params_path"    : "params_multigrid",
        "pimsolver_params_path"    : "params_pimsolver",
        "iotrunk_params_path"      : "params_iotrunk",
        "penalisation_params_path" : "params_penalisation",
        "diags_params_path"        : "params_diags",
        "tempdev_params_path"      : "params_temp_dev",
        "neutrals_params_path"     : "params_neutrals"
    }

    equi_params_dict = {
        "equi_numerical_params": "NUMERICAL",
        "equi_carthy_params": "CARTHY",
        "equi_cerfons_params": "CERFONS",
        "equi_circular_params": "CIRCULAR",
        "equi_slab_params": "SLAB"
    }
    
    def __init__(self, namelist_dict):
        super().__init__(namelist_dict)
    
    @classmethod
    def from_parameter_file(cls, filename):
        root_namelist = cls.cleaned_read(filename)
        try:
            for equi_parameter_group in cls.equi_params_dict.keys():
                if root_namelist[equi_parameter_group]:
                    root_namelist["equi_params"] = root_namelist[equi_parameter_group]
                    equi_type = cls.equi_params_dict[equi_parameter_group]
        except KeyError:
            pass
        
        # Checks the 'params_filepaths' group and replaces any sections found
        unique_params_filepaths = set(root_namelist['params_filepaths'].values())

        for params_file in unique_params_filepaths:
            params_namelist = cls.cleaned_read(Path(filename.parent / params_file).absolute())

            for key, file_pointer in root_namelist['params_filepaths'].items():
                if file_pointer == params_file:
                    try:
                        if key != "equi_init_params_path":
                            parameter_group = cls.params_filepath_dict[key.lower()]
                            root_namelist[parameter_group] = params_namelist[parameter_group]
                        else:
                            for equi_parameter_group in cls.equi_params_dict.keys():
                                if params_namelist[equi_parameter_group]:
                                    root_namelist["equi_params"] = params_namelist[equi_parameter_group]
                                    equi_type = cls.equi_params_dict[equi_parameter_group]
                            
                    except KeyError:
                        # print("\t\t{} not found in pointer namelist. Setting group to blank".format(parameter_group))
                        root_namelist[parameter_group] = {}
        
        if not(root_namelist["equi_params"]):
            raise NotImplementedError("No parameter group corresponding to an implemented equilibrium type was found in parameters")
        
        return cls(root_namelist), equi_type
    