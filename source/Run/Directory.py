from source import Path, np, time, os
from source.shared import NetCDFPath, UserEnvironment
from .Parameters import Parameters

class Directory:
    
    run_files = {
        "main_grid_file": "vgrid.nc",
        "perp_grid_file": "perpghost.nc",
        "parameter_file": "params.in",
        "scalar_diags_file": "diagnostics_scalar.nc",
        "zonal_diags_file": "diagnostics_zonal.nc",
        "penalisation_file": "trunk/pen_metainfo.nc",
        "divertor_points_file": "trunk/divertor_points.nc",
        "exclusion_points_file": "trunk/exclusion_points.nc",
        "equi_storage_file": "trunk/equi_storage.nc",
        "normalisation_file": "physical_parameters.nml",
        "map_metadata_file": "trunk/map_metainfo.nc",
        "f2s_map_forward_file": "trunk/map_Qmap1.nc",
        "f2s_map_reverse_file": "trunk/map_Qmap2.nc",
        "s2f_map_forward_file": "trunk/map_Imap1.nc",
        "s2f_map_reverse_file": "trunk/map_Imap2.nc"
    }
    
    def __init__(self, filepath):
        self.filepath = self.__check_directory_exists(filepath)
        self.use_error_snaps = False
        self.filepath_given = filepath
    
    @classmethod
    def initialise_and_read_parameters(cls, filepath):
        print("Initialising RunDirectory object")
        start_time = time.time()

        self = cls(filepath)
        
        self.check_snaps()
        [parameters, equi_type] = self.check_directory()
        
        stop_time = time.time()
        print("RunDirectory object is ready to use ({:5.2f}s elapsed)".format(stop_time-start_time))
        
        return self, parameters, equi_type
        
    def check_snaps(self):
        snaps_in_dir = 0
        error_snaps_in_dir = 0
        neutral_snaps_in_dir = 0
        neutral_error_snaps_in_dir = 0

        for filename in os.listdir(self.filepath):
            if filename.startswith("snaps") and filename.endswith(".nc"):
                snaps_in_dir += 1
            if filename.startswith("error_snaps") and filename.endswith(".nc"):
                error_snaps_in_dir += 1
            if filename.startswith("neutral_snaps") and filename.endswith(".nc"):
                neutral_snaps_in_dir += 1
            if filename.startswith("neutrals_error_snaps") and filename.endswith(".nc"):
                neutral_error_snaps_in_dir += 1
            
        print(f"\tSnaps in directory: {snaps_in_dir}")
        print(f"\tError snaps in directory: {error_snaps_in_dir}")
        print(f"\tNeutral snaps in directory: {neutral_snaps_in_dir}")
        print(f"\tNeutral error snaps in directory: {neutral_error_snaps_in_dir}")
        
        self.snaps = np.zeros((snaps_in_dir,), dtype=NetCDFPath)
               
        for snap in range(snaps_in_dir):
            self.snaps[snap] = NetCDFPath(self.filepath / f"snaps{snap:05d}.nc")
            assert(self.snaps[snap].exists())

        if error_snaps_in_dir > 0:
            self.error_snaps = np.zeros((error_snaps_in_dir,), dtype=NetCDFPath)
            for error_snap in range(error_snaps_in_dir):
                self.error_snaps[error_snap] = NetCDFPath(self.filepath / f"error_snaps{error_snap:05d}.nc")
                assert(self.error_snaps[error_snap].exists())
        
        if neutral_snaps_in_dir > 0:
            self.neutral_snaps = np.zeros((neutral_snaps_in_dir,), dtype=NetCDFPath)
            for neutral_snap in range(neutral_snaps_in_dir):
                self.neutral_snaps[neutral_snap] = NetCDFPath(self.filepath / f"neutral_snaps{neutral_snap:05d}.nc")
                assert(self.neutral_snaps[neutral_snap].exists())

        if neutral_error_snaps_in_dir > 0:
            self.neutral_error_snaps = np.zeros((neutral_error_snaps_in_dir,), dtype=NetCDFPath)
            for neutral_error_snap in range(neutral_error_snaps_in_dir):
                self.neutral_error_snaps[neutral_error_snap] = NetCDFPath(self.filepath / f"neutrals_error_snaps{neutral_error_snap:05d}.nc")
                assert(self.neutral_error_snaps[neutral_error_snap].exists())
        
    def check_directory(self):
        for attribute, filename in self.run_files.items():
            
            datapath = Path(self.filepath / filename)
            setattr(self, attribute, NetCDFPath(datapath) if filename.endswith(".nc") else datapath)
            print(f"\t{attribute:30} -> {filename:30} exists: {datapath.exists()}")
            
            # Use trunk fallback for the grids
            if not(datapath.exists()) and (attribute in {"main_grid_file", "perp_grid_file"}):
                fallback_filename = f"trunk/mgrid_{filename.replace('.nc','')}_lvl001.nc"
                
                fallback = Path(self.filepath / fallback_filename)
                if fallback.exists():
                    setattr(self, attribute, NetCDFPath(fallback) if fallback_filename.endswith(".nc") else fallback)
                    print(f"\t{'fallback '+attribute:30} -> {fallback_filename:30} exists: {fallback.exists()}")
            
            if not(datapath.exists()) and (attribute in {"normalisation_file"}):
                # Check the parent directory
                
                fallback = Path(self.filepath.parent / filename)
                if fallback.exists():
                    setattr(self, attribute, NetCDFPath(fallback) if filename.endswith(".nc") else fallback)
                    print(f"\t{'fallback '+attribute:30} -> {filename:30} exists: {fallback.exists()}")
            
            if attribute == "parameter_file":
                if self.parameter_file.exists():
                    [parameters, equi_type] = Parameters.from_parameter_file(self.parameter_file)
                else:
                    raise FileNotFoundError("Parameter file is required")
                
                if equi_type == "NUMERICAL":
                    netcdf_path = Path(parameters["equi_params"]["path_to_netcdf"])/Path(parameters["equi_params"]["equilibrium_case"]+".nc")
                    self.equilibrium_netcdf = NetCDFPath((self.filepath / netcdf_path).absolute())
                    
                    print(f"\t{'equilibrium_netcdf':30} -> {str(netcdf_path):30} exists: {self.equilibrium_netcdf.exists()}")
                    assert(self.equilibrium_netcdf.exists())
        
        return parameters, equi_type
    
    def __check_directory_exists(self, filepath):
        
        path = Path(filepath).expanduser().absolute()
        
        if path.exists() and path.is_dir():
            print(f"Filepath set to {path}")
            return path
        else:
            print(f"Filepath {path} does not exist. Testing fallbacks")
            return self.__test_filepath_fallbacks(Path(filepath).expanduser())
    
    def __test_filepath_fallbacks(self, path):
        usrenv = UserEnvironment()
        
        default_run_directory = Path(usrenv.default_run_directory)
        defaultpath = default_run_directory / path
        
        if defaultpath.exists() and defaultpath.is_dir():
            print(f"\tFilepath set to {defaultpath}")
            return defaultpath
        else:
            raise FileNotFoundError(f"Filepath {defaultpath} is not valid")
    
    def __str__(self):
        return_string = ""
        
        for attribute, value in self.__dict__.items():
            if type(value) == np.ndarray:
                if value.size > 0:
                    return_string += f"\t{attribute:30} -> array of len({len(value)}) starting at {str(value[0])}\n"
                else:
                    return_string += f"\t{attribute:30} -> empty\n"
            else:
                return_string += f"\t{attribute:30} -> {str(value):30} \n"

        return return_string
    