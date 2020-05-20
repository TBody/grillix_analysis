from .components import NamelistReader
from source import unit_registry, Quantity, np

class Normalisation():
    # See https://unidata.github.io/MetPy/latest/tutorials/unit_tutorial.html
    
    normalisation_parameters = {"case_name", "b0", "te0", "ti0", "n0", "r0", "mi", "z", "z_eff", "neutral_density", "sigma_cx"}
    
    def __init__(self, normalisation_file, with_print=False):
        
        self.namelist_dict = NamelistReader.cleaned_read(normalisation_file)
        
        for parameter in self.normalisation_parameters:
            if parameter is "sigma_cx" or parameter is "neutral_density":
                continue
            else:
                assert parameter in self.namelist_dict['physical_parameters'].keys(), f"parameter '{parameter}' missing from physical parameters"
        
        # Magnetic field normalisation, usually taken on axis, in Tesla
        self.B0    = Quantity(self.namelist_dict['physical_parameters']['b0'], unit_registry.tesla)
        # Electron temperature normalisation, in electron-volts
        self.Te0   = Quantity(self.namelist_dict['physical_parameters']['te0'], unit_registry.electron_volt)
        # Ion temperature normalisation, in electron-volts
        self.Ti0   = Quantity(self.namelist_dict['physical_parameters']['ti0'], unit_registry.electron_volt)
        # Density normalisation, in particles-per-cubic-metres
        self.n0    = Quantity(self.namelist_dict['physical_parameters']['n0'], unit_registry.metre**-3)
        # Major radius, in metres (n.b. this is also the scale length for parallel quantities)
        self.R0    = Quantity(self.namelist_dict['physical_parameters']['r0'], unit_registry.metre)
        # Ion mass, in amu
        self.Mi    = Quantity(self.namelist_dict['physical_parameters']['mi'], unit_registry.amu)
        # Ion charge, in e
        self.Z     = Quantity(self.namelist_dict['physical_parameters']['z'], unit_registry.elementary_charge)
        # Ion effective charge, in e
        self.Z_eff = Quantity(self.namelist_dict['physical_parameters']['z_eff'], unit_registry.elementary_charge)

        self.write_constants()
        self.calculate_dependent_parameters()

        for parameter, value in self.namelist_dict['physical_parameters'].items():
            if parameter not in self.normalisation_parameters:
                print(f"Additional parameter {parameter} given in namelist")
                if parameter in self.__dict__.keys():
                    previous_value = getattr(self, parameter)
                    print(f"Overwriting the value of {parameter} from {previous_value} to {value}")
                    setattr(self, parameter, Quantity(value, previous_value.units))
                else:
                    raise NotImplementedError(f"Additional parameter {parameter} cannot be used")
        
        self.calculate_dimensionless_parameters()
        
        # If both neutral_density and sigma_cx are given, calculate neutral parameters as well
        try:
            self.neutral0 = Quantity(self.namelist_dict['physical_parameters']['neutral_density'], unit_registry.metre**-3)
            self.sigma_cx = Quantity(self.namelist_dict['physical_parameters']['sigma_cx'], unit_registry.metre**2)
            self.calculate_neutral_parameters()
        except KeyError:
            print("Neutrals parameters will not be set")

        if with_print:
            print(self)
        
    def __str__(self):
        
        string = f"\t{'Value':<30}\t{'Magnitude':<10}\t{'Units':<20}\n"
        for parameter_name, parameter in self.__dict__.items():
            if type(parameter) == Quantity:
                string += f"\t{parameter_name:<30}\t{parameter.magnitude:<10.4e}\t{parameter.units:<20}\n"
        
        return string
    
    def write_constants(self):
        self.electron_to_proton_mass_ratio = Quantity(1836.15267343, '')
        self.electron_charge = Quantity(1.0, unit_registry.elementary_charge)
        self.proton_mass = Quantity(1.0, unit_registry.amu)
        self.speed_of_light = Quantity(1.0, unit_registry.speed_of_light)
        self.vacuum_permeability = Quantity(1.25663706212e-6, unit_registry.henry/unit_registry.meter)
    
    def calculate_dependent_parameters(self):
        # Ion Larmor Radius [m] (n.b. this is also the scale length for perpendicular quantities)
        self.rho_s0 = (np.sqrt(self.Ti0*self.Mi)/(self.electron_charge*self.B0)).to_base_units()
        # Sound speed [m/s]
        self.c_s0 = (np.sqrt(self.Te0/self.Mi)).to_base_units()
        # Alfven speed [m/s]
        self.v_A0 = (self.B0/np.sqrt(self.vacuum_permeability*self.n0*self.Mi)).to_base_units()
        # Time normalisation [s]
        self.tau_0 = (self.R0/self.c_s0).to(unit_registry.seconds)
        
        # Unitless cgs values
        n0_cm3                 = self.n0.to(unit_registry.cm**-3).magnitude
        Te0_eV                 = self.Te0.to(unit_registry.eV).magnitude
        zeta                   = (self.Ti0/self.Te0).to('')
        Z_eff                  = self.Z_eff.magnitude
        Z                      = self.Z.magnitude
        Mi_amu                 = self.Mi.to(unit_registry.amu).magnitude
        # Coloumb logarithm [-]
        self.Coloumb_logarithm = 24 - np.log(np.sqrt(n0_cm3)/Te0_eV)
        # Tau_e [s] (Electron-ion collisionality calculated with Z_eff)
        self.tau_e             = Quantity(344000*(Te0_eV**(3/2))/(n0_cm3*self.Coloumb_logarithm*Z_eff), unit_registry.seconds)
        # Tau_e [s] (Electron-ion collisionality calculated without Z_eff)
        self.tau_e_nozeff      = Quantity(344000*(Te0_eV**(3/2))/(n0_cm3*self.Coloumb_logarithm*Z), unit_registry.seconds)
        # Tau_i [s] (Ion-electron collisionality calculated from tau_e_nozeff)
        self.tau_i             = self.tau_e_nozeff/(Z**2)*(zeta**1.5)*np.sqrt(2.0*Mi_amu*self.electron_to_proton_mass_ratio )
    
    def calculate_dimensionless_parameters(self):
        self.delta = self.rho_s0 / self. R0
        self.beta_0 = self.c_s0 ** 2 / (self.v_A0 **2)
        self.mu = (self.Mi.to(unit_registry.amu).magnitude * self.electron_to_proton_mass_ratio)**-1
        self.zeta = self.Ti0/self.Te0
        self.Te0_norm = self.tau_e * self.c_s0 / self.R0
        self.Ti0_norm = self.tau_i * self.c_s0 / self.R0
        self.nu_e0 = self.Te0_norm ** -1
        self.nu_i0 = self.Ti0_norm ** -1
        self.chipar_e = 3.16 * self.Te0_norm * self.mu**-1
        self.chipar_i = 3.90 * self.zeta * self.Ti0_norm
        self.etapar_e = 0.51 * self.nu_e0 * self.mu
        self.etapar_i = 0.96 * self.Ti0_norm
    
    def calculate_neutral_parameters(self):
        # Add neutral-specific parameters
        # reference neutral density, normalised to plasma density
        self.N0_init = self.neutral0/self.n0
        # reference temperature, in eV
        self.Tref = self.Te0.to('eV')
        # reference density, in cm^-3
        self.nref = self.n0.to('cm^-3')
        # reference rate coefficient, in cm^3 / s
        self.kref = (self.c_s0 / (self.R0 * self.n0)).to('cm^3/s')
        # reference electron cooling rate coefficient, in eV cm^3 / s
        self.Wref = self.Te0*self.kref
        # charge exchange cross-section
        self.s_cx = self.sigma_cx*self.R0*self.n0