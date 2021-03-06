from . import StaticVariable
from source import defaultdict

class District(StaticVariable):
    
    district_dict = defaultdict(list, {
        813: "DISTRICT_CORE",
        # point located in core (outside actual computational domain, rho<rhomin)
        814: "DISTRICT_CLOSED",
        # point located in closed field line region (within computational domain)
        815: "DISTRICT_SOL",
        # point located in scrape-off layer (within computational domain)
        816: "DISTRICT_PRIVFLUX",
        # point located in private flux region (within computational domain)
        817: "DISTRICT_WALL",
        # point located in wall (outside computational domain, rho>rhomax)
        818: "DISTRICT_DOME",
        # point located in divertor dome (outside computational domain, e.g. rho<rhomin_privflux)
        819: "DISTRICT_OUT",
        # point located outside additional masks, i.e. shadow region (outside computational domain)
    })

    inv_district_dict = {value : key for (key, value) in district_dict.items()}
    
    def __init__(self, run=None):
        netcdf_filename = "equi_storage_file"
        title = "District"
        self.numerical_variable = False
        super().__init__('district', netcdf_filename, title, run=run)
    
    def __format_value__(self, value, run=None):
        return self.district_dict[value]