from source import np
from source.Variable import Variable
import re as regex

class DiagnosticScalarVariable(Variable):
    # Any variable defined in terms of terms written into diagnostics_scalar.nc
    
    def __init__(self, index_in_netcdf, **kwargs):
        self.index_in_netcdf = index_in_netcdf
        
        super().__init__(**kwargs)

        if not(hasattr(self, 'title')):
            class_name = regex.split('(?=[A-Z])', self.__class__.__name__)
            self.title = " ".join(class_name)
    
    def update_run_values(self):
        self.diagnostic_netcdf = self.run.directory.scalar_diags_file

    def values(self, time_slice=slice(None), *args):
        
        z = self.diagnostic_netcdf['diags'][time_slice, self.index_in_netcdf-1]
        
        return z
    
    def __call__(self, time_slice=None, toroidal_slice=None, poloidal_slice=slice(None)):
        
        values = self.values
        
        return np.atleast_3d(values).reshape((1,1,-1))

class Time(DiagnosticScalarVariable):

    def __init__(self, **kwargs):
        index_in_netcdf = 1
        
        super().__init__(index_in_netcdf, **kwargs)
    
    def update_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.tau_0

class Timestep(DiagnosticScalarVariable):

    def __init__(self, **kwargs):
        index_in_netcdf = 2
        
        super().__init__(index_in_netcdf, **kwargs)
    
    def update_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.tau_0

class AverageDensity(DiagnosticScalarVariable):

    def __init__(self, **kwargs):
        index_in_netcdf = 11
        self.title = "Density"
        
        super().__init__(index_in_netcdf, **kwargs)
    
    def update_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.n0

class AverageElectronTemperature(DiagnosticScalarVariable):

    def __init__(self, **kwargs):
        index_in_netcdf = 12
        self.title = "ETemp"

        super().__init__(index_in_netcdf, **kwargs)
    
    def update_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.Te0

class AverageIonTemperature(DiagnosticScalarVariable):

    def __init__(self, **kwargs):
        index_in_netcdf = 13
        self.title = "ITemp"
        
        super().__init__(index_in_netcdf, **kwargs)
    
    def update_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.Ti0

class AverageScalarPotential(DiagnosticScalarVariable):

    def __init__(self, **kwargs):
        index_in_netcdf = 14
        self.title = "Phi"
        
        super().__init__(index_in_netcdf, **kwargs)
    
    def update_normalisation_factor(self):
        self.normalisation_factor = (self.normalisation.Te0/self.normalisation.electron_charge).to("kilovolt")

class AverageVorticity(DiagnosticScalarVariable):

    def __init__(self, **kwargs):
        index_in_netcdf = 15
        self.title = "Vort"
        
        super().__init__(index_in_netcdf, **kwargs)
    
    def update_normalisation_factor(self):
        self.normalisation_factor = (
            self.normalisation.Mi * self.normalisation.n0 * self.normalisation.Te0
            /(self.normalisation.electron_charge * self.normalisation.rho_s0**2 * self.normalisation.B0**2 )
        ).to('coulomb/meter**3')

class AverageParallelCurrent(DiagnosticScalarVariable):

    def __init__(self, **kwargs):
        index_in_netcdf = 16
        self.title = "Jpar"
        
        super().__init__(index_in_netcdf, **kwargs)
    
    def update_normalisation_factor(self):
        self.normalisation_factor = (self.normalisation.c_s0 * self.normalisation.electron_charge * self.normalisation.n0).to(
            'kiloampere*meter**-2'
        )

class AverageParallelIonVelocity(DiagnosticScalarVariable):

    def __init__(self, **kwargs):
        index_in_netcdf = 17
        self.title = "Upar"
        
        super().__init__(index_in_netcdf, **kwargs)
    
    def update_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.c_s0.to('kilometers/second')

class AverageParallelVectorPotential(DiagnosticScalarVariable):

    def __init__(self, **kwargs):
        index_in_netcdf = 18
        self.title = "Apar"
        
        super().__init__(index_in_netcdf, **kwargs)
    
    def update_normalisation_factor(self):
    
        self.normalisation_factor = self.normalisation.beta_0 * self.normalisation.B0 * self.normalisation.rho_s0

class AveragePerpendicularKineticEnergy(DiagnosticScalarVariable):

    def __init__(self, **kwargs):
        index_in_netcdf = 21
        self.title = "K.E. perp"
        
        super().__init__(index_in_netcdf, **kwargs)
        
class AverageParallelKineticEnergy(DiagnosticScalarVariable):

    def __init__(self, **kwargs):
        index_in_netcdf = 22
        self.title = "K.E. par"
        
        super().__init__(index_in_netcdf, **kwargs)
        
class AverageElectronThermalEnergy(DiagnosticScalarVariable):

    def __init__(self, **kwargs):
        index_in_netcdf = 23
        self.title = "T.E. e"
        
        super().__init__(index_in_netcdf, **kwargs)

class AverageIonThermalEnergy(DiagnosticScalarVariable):

    def __init__(self, **kwargs):
        index_in_netcdf = 24
        self.title = "T.E. i"
        
        super().__init__(index_in_netcdf, **kwargs)
        
class AverageMagneticEnergy(DiagnosticScalarVariable):

    def __init__(self, **kwargs):
        index_in_netcdf = 25
        self.title = "Mag.E."
        
        super().__init__(index_in_netcdf, **kwargs)
        
class AverageParallelKineticElectronEnergy(DiagnosticScalarVariable):

    def __init__(self, **kwargs):
        index_in_netcdf = 26
        self.title = "K.E. par e"
        
        super().__init__(index_in_netcdf, **kwargs)
        
class DerivativeDensity(DiagnosticScalarVariable):

    def __init__(self, **kwargs):
        index_in_netcdf = 31
        self.title = "d/dt Density"
        
        super().__init__(index_in_netcdf, **kwargs)
        
class DerivativePerpendicularKineticEnergy(DiagnosticScalarVariable):

    def __init__(self, **kwargs):
        index_in_netcdf = 32
        self.title = "d/dt K.E. perp"
        
        super().__init__(index_in_netcdf, **kwargs)

class DerivativeParallelKineticEnergy(DiagnosticScalarVariable):

    def __init__(self, **kwargs):
        index_in_netcdf = 33
        self.title = "d/dt K.E. par"
        
        super().__init__(index_in_netcdf, **kwargs)

class DerivativeElectronThermalEnergy(DiagnosticScalarVariable):

    def __init__(self, **kwargs):
        index_in_netcdf = 34
        self.title = "d/dt T.E. e"
        
        super().__init__(index_in_netcdf, **kwargs)

class DerivativeIonThermalEnergy(DiagnosticScalarVariable):

    def __init__(self, **kwargs):
        index_in_netcdf = 35
        self.title = "d/dt T.E. i"
        
        super().__init__(index_in_netcdf, **kwargs)

class DerivativeMagneticEnergy(DiagnosticScalarVariable):

    def __init__(self, **kwargs):
        index_in_netcdf = 36
        self.title = "d/dt Mag.E."
        
        super().__init__(index_in_netcdf, **kwargs)

class DerivativeParallelKineticElectronEnergy(DiagnosticScalarVariable):

    def __init__(self, **kwargs):
        index_in_netcdf = 37
        self.title = "d/dt K.E. par e"
        
        super().__init__(index_in_netcdf, **kwargs)

class ParticleSource(DiagnosticScalarVariable):

    def __init__(self, **kwargs):
        index_in_netcdf = 41
        self.title = "Source"
        
        super().__init__(index_in_netcdf, **kwargs)
        
class ParticleSink(DiagnosticScalarVariable):
    # Particle Sink (due to diffusion/dissipation at boundaries)

    def __init__(self, **kwargs):
        index_in_netcdf = 42
        self.title = "Sink"
        
        super().__init__(index_in_netcdf, **kwargs)
        
class TransferTermOfEperpAndEthe(DiagnosticScalarVariable):
    # "Jpar*Grad_par(Pot)"
    def __init__(self, **kwargs):
        index_in_netcdf = 51
        self.title = "E perp -> Ethe"
        
        super().__init__(index_in_netcdf, **kwargs)
            
class TransferTermOfEperpFromTe(DiagnosticScalarVariable):
    # Nea*Tea*Div(V_e)
    def __init__(self, **kwargs):
        index_in_netcdf = 52
        self.title = "Te -> E perp "
        
        super().__init__(index_in_netcdf, **kwargs)
        
class TransferTermOfEparFromTe(DiagnosticScalarVariable):
    # -Upar*Grad_par(Nea*Tea)>
    def __init__(self, **kwargs):
        index_in_netcdf = 53
        self.title = "Te -> E par"
        
        super().__init__(index_in_netcdf, **kwargs)
        
class TransferTermOfEthe1(DiagnosticScalarVariable):
    # Vpar*Grad_par(Nea*Tea)>
    def __init__(self, **kwargs):
        index_in_netcdf = 54
        self.title = "E the 1"
        
        super().__init__(index_in_netcdf, **kwargs)
            
class TransferTermOfEthe2(DiagnosticScalarVariable):
    # Etapar/Jpar^2/(Tea^(3/2))>
    def __init__(self, **kwargs):
        index_in_netcdf = 55
        self.title = "E the 2"
        
        super().__init__(index_in_netcdf, **kwargs)
        
class TransferTermOfEthe3(DiagnosticScalarVariable):
    # -0.71*Jpar*Grad_par(Tea)
    def __init__(self, **kwargs):
        index_in_netcdf = 56
        self.title = "E the 3"
        
        super().__init__(index_in_netcdf, **kwargs)
        
class TransferTermOfEperpFromTi(DiagnosticScalarVariable):
    # Nea*Tia*Div(V_e)
    def __init__(self, **kwargs):
        index_in_netcdf = 57
        self.title = "Ti -> E perp"
        
        super().__init__(index_in_netcdf, **kwargs)
        
class TransferTermOfEparFromTi(DiagnosticScalarVariable):
    # -Upar*Grad_par(Nea*Tia)
    def __init__(self, **kwargs):
        index_in_netcdf = 58
        self.title = "Ti -> E par"
        
        super().__init__(index_in_netcdf, **kwargs)
        
class DissipSourceOfEperp(DiagnosticScalarVariable):
    # - Pot*Dw + (1-Bsq)>*|Nabla_perp(Pot)|^2 / (2b^2) * (Dn+Sn-Dw)
    def __init__(self, **kwargs):
        index_in_netcdf = 61
        self.title = "Eperp"
        
        super().__init__(index_in_netcdf, **kwargs)
        
class DissipSourceOfEpar(DiagnosticScalarVariable):
    # Nea*Upar*Su + Nea*Upar*Du< + >Upar^2/2*(Dn+Sn-Dw)
    def __init__(self, **kwargs):
        index_in_netcdf = 62
        self.title = "Epar"
        
        super().__init__(index_in_netcdf, **kwargs)
        
class DissipSourceOfEthe(DiagnosticScalarVariable):
    # 3/2*Tea*(Dn+Sn) + 3/2*Nea*(Dte+Ste)
    def __init__(self, **kwargs):
        index_in_netcdf = 63
        self.title = "Ethe"
        
        super().__init__(index_in_netcdf, **kwargs)
        
class DissipSourceOfEemAndEpare(DiagnosticScalarVariable):
    # 1/2*Mu*(Jpar/Nea)^2 * (Dn+Sn)
    def __init__(self, **kwargs):
        index_in_netcdf = 64
        self.title = "Eem+Epare"
        
        super().__init__(index_in_netcdf, **kwargs)
        
class DissipSourceOfEthi(DiagnosticScalarVariable):
    # 3/2*Tia*(Dn+Sn) + 3/2*Nea*(Dti+Sti)
    def __init__(self, **kwargs):
        index_in_netcdf = 65
        self.title = "Ethi"
        
        super().__init__(index_in_netcdf, **kwargs)
        
class NeutralsDensity(DiagnosticScalarVariable):

    def __init__(self, **kwargs):
        index_in_netcdf = 71
        self.title = "N Dens"
        
        super().__init__(index_in_netcdf, **kwargs)
    
    def update_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.n0
        
class IonizationDensitySource(DiagnosticScalarVariable):

    def __init__(self, **kwargs):
        index_in_netcdf = 72
        self.title = "Iz src"
        
        super().__init__(index_in_netcdf, **kwargs)
        
class IonizationCooling(DiagnosticScalarVariable):

    def __init__(self, **kwargs):
        index_in_netcdf = 73
        self.title = "Iz cooling"
        
        super().__init__(index_in_netcdf, **kwargs)
        
class CXFrictionOnParallelIonVelocity(DiagnosticScalarVariable):

    def __init__(self, **kwargs):
        index_in_netcdf = 74
        self.title = "CX on Upar"
        
        super().__init__(index_in_netcdf, **kwargs)
        
class CXFrictionOnVorticity(DiagnosticScalarVariable):

    def __init__(self, **kwargs):
        index_in_netcdf = 75
        self.title = "CX on Vort"
        
        super().__init__(index_in_netcdf, **kwargs)
        
class DerivativeNeutralsDensity(DiagnosticScalarVariable):

    def __init__(self, **kwargs):
        index_in_netcdf = 76
        self.title = "d/dt  N Dens"
        
        super().__init__(index_in_netcdf, **kwargs)
        