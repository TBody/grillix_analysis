from source import np
from .. import Variable
import re as regex

class DiagnosticScalarVariable(Variable):
    # Any variable defined in terms of terms written into diagnostics_scalar.nc
    
    def __init__(self, index_in_netcdf, run=None):
        self.index_in_netcdf = index_in_netcdf
        
        super().__init__(run=run)

        if not(hasattr(self, 'title')):
            class_name = regex.split('(?=[A-Z])', self.__class__.__name__)
            title = " ".join(class_name)
    
    def set_run(self):
        self.diagnostic_netcdf = self.run.directory.scalar_diags_file

    def values(self, time_slice=slice(None), *args):
        
        z = self.diagnostic_netcdf['diags'][time_slice, self.index_in_netcdf-1]
        
        return z
    
    def __call__(self, time_slice=None, toroidal_slice=None, poloidal_slice=slice(None)):
        
        values = self.values
        
        return np.atleast_3d(values).reshape((1,1,-1))

class Time(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 1
        
        super().__init__(index_in_netcdf, run=run)
    
    def update_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.tau_0

class Timestep(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 2
        
        super().__init__(index_in_netcdf, run=run)
    
    def update_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.tau_0

class AverageDensity(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 11
        title = "Density"
        
        super().__init__(index_in_netcdf, run=run)
    
    def update_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.n0

class AverageElectronTemperature(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 12
        title = "ETemp"

        super().__init__(index_in_netcdf, run=run)
    
    def update_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.Te0

class AverageIonTemperature(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 13
        title = "ITemp"
        
        super().__init__(index_in_netcdf, run=run)
    
    def update_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.Ti0

class AverageScalarPotential(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 14
        title = "Phi"
        
        super().__init__(index_in_netcdf, run=run)
    
    def update_normalisation_factor(self):
        self.normalisation_factor = (self.normalisation.Te0/self.normalisation.electron_charge).to("kilovolt")

class AverageVorticity(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 15
        title = "Vort"
        
        super().__init__(index_in_netcdf, run=run)
    
    def update_normalisation_factor(self):
        self.normalisation_factor = (
            self.normalisation.Mi * self.normalisation.n0 * self.normalisation.Te0
            /(self.normalisation.electron_charge * self.normalisation.rho_s0**2 * self.normalisation.B0**2 )
        ).to('coulomb/meter**3')

class AverageParallelCurrent(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 16
        title = "Jpar"
        
        super().__init__(index_in_netcdf, run=run)
    
    def update_normalisation_factor(self):
        self.normalisation_factor = (self.normalisation.c_s0 * self.normalisation.electron_charge * self.normalisation.n0).to(
            'kiloampere*meter**-2'
        )

class AverageParallelIonVelocity(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 17
        title = "Upar"
        
        super().__init__(index_in_netcdf, run=run)
    
    def update_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.c_s0.to('kilometers/second')

class AverageParallelVectorPotential(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 18
        title = "Apar"
        
        super().__init__(index_in_netcdf, run=run)
    
    def update_normalisation_factor(self):
    
        self.normalisation_factor = self.normalisation.beta_0 * self.normalisation.B0 * self.normalisation.rho_s0

class AveragePerpendicularKineticEnergy(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 21
        title = "K.E. perp"
        
        super().__init__(index_in_netcdf, run=run)
        
class AverageParallelKineticEnergy(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 22
        title = "K.E. par"
        
        super().__init__(index_in_netcdf, run=run)
        
class AverageElectronThermalEnergy(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 23
        title = "T.E. e"
        
        super().__init__(index_in_netcdf, run=run)

class AverageIonThermalEnergy(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 24
        title = "T.E. i"
        
        super().__init__(index_in_netcdf, run=run)
        
class AverageMagneticEnergy(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 25
        title = "Mag.E."
        
        super().__init__(index_in_netcdf, run=run)
        
class AverageParallelKineticElectronEnergy(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 26
        title = "K.E. par e"
        
        super().__init__(index_in_netcdf, run=run)
        
class DerivativeDensity(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 31
        title = "d/dt Density"
        
        super().__init__(index_in_netcdf, run=run)
        
class DerivativePerpendicularKineticEnergy(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 32
        title = "d/dt K.E. perp"
        
        super().__init__(index_in_netcdf, run=run)

class DerivativeParallelKineticEnergy(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 33
        title = "d/dt K.E. par"
        
        super().__init__(index_in_netcdf, run=run)

class DerivativeElectronThermalEnergy(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 34
        title = "d/dt T.E. e"
        
        super().__init__(index_in_netcdf, run=run)

class DerivativeIonThermalEnergy(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 35
        title = "d/dt T.E. i"
        
        super().__init__(index_in_netcdf, run=run)

class DerivativeMagneticEnergy(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 36
        title = "d/dt Mag.E."
        
        super().__init__(index_in_netcdf, run=run)

class DerivativeParallelKineticElectronEnergy(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 37
        title = "d/dt K.E. par e"
        
        super().__init__(index_in_netcdf, run=run)

class ParticleSource(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 41
        title = "Source"
        
        super().__init__(index_in_netcdf, run=run)
        
class ParticleSink(DiagnosticScalarVariable):
    # Particle Sink (due to diffusion/dissipation at boundaries)

    def __init__(self, run=None):
        index_in_netcdf = 42
        title = "Sink"
        
        super().__init__(index_in_netcdf, run=run)
        
class TransferTermOfEperpAndEthe(DiagnosticScalarVariable):
    # "Jpar*Grad_par(Pot)"
    def __init__(self, run=None):
        index_in_netcdf = 51
        title = "E perp -> Ethe"
        
        super().__init__(index_in_netcdf, run=run)
            
class TransferTermOfEperpFromTe(DiagnosticScalarVariable):
    # Nea*Tea*Div(V_e)
    def __init__(self, run=None):
        index_in_netcdf = 52
        title = "Te -> E perp "
        
        super().__init__(index_in_netcdf, run=run)
        
class TransferTermOfEparFromTe(DiagnosticScalarVariable):
    # -Upar*Grad_par(Nea*Tea)>
    def __init__(self, run=None):
        index_in_netcdf = 53
        title = "Te -> E par"
        
        super().__init__(index_in_netcdf, run=run)
        
class TransferTermOfEthe1(DiagnosticScalarVariable):
    # Vpar*Grad_par(Nea*Tea)>
    def __init__(self, run=None):
        index_in_netcdf = 54
        title = "E the 1"
        
        super().__init__(index_in_netcdf, run=run)
            
class TransferTermOfEthe2(DiagnosticScalarVariable):
    # Etapar/Jpar^2/(Tea^(3/2))>
    def __init__(self, run=None):
        index_in_netcdf = 55
        title = "E the 2"
        
        super().__init__(index_in_netcdf, run=run)
        
class TransferTermOfEthe3(DiagnosticScalarVariable):
    # -0.71*Jpar*Grad_par(Tea)
    def __init__(self, run=None):
        index_in_netcdf = 56
        title = "E the 3"
        
        super().__init__(index_in_netcdf, run=run)
        
class TransferTermOfEperpFromTi(DiagnosticScalarVariable):
    # Nea*Tia*Div(V_e)
    def __init__(self, run=None):
        index_in_netcdf = 57
        title = "Ti -> E perp"
        
        super().__init__(index_in_netcdf, run=run)
        
class TransferTermOfEparFromTi(DiagnosticScalarVariable):
    # -Upar*Grad_par(Nea*Tia)
    def __init__(self, run=None):
        index_in_netcdf = 58
        title = "Ti -> E par"
        
        super().__init__(index_in_netcdf, run=run)
        
class DissipSourceOfEperp(DiagnosticScalarVariable):
    # - Pot*Dw + (1-Bsq)>*|Nabla_perp(Pot)|^2 / (2b^2) * (Dn+Sn-Dw)
    def __init__(self, run=None):
        index_in_netcdf = 61
        title = "Eperp"
        
        super().__init__(index_in_netcdf, run=run)
        
class DissipSourceOfEpar(DiagnosticScalarVariable):
    # Nea*Upar*Su + Nea*Upar*Du< + >Upar^2/2*(Dn+Sn-Dw)
    def __init__(self, run=None):
        index_in_netcdf = 62
        title = "Epar"
        
        super().__init__(index_in_netcdf, run=run)
        
class DissipSourceOfEthe(DiagnosticScalarVariable):
    # 3/2*Tea*(Dn+Sn) + 3/2*Nea*(Dte+Ste)
    def __init__(self, run=None):
        index_in_netcdf = 63
        title = "Ethe"
        
        super().__init__(index_in_netcdf, run=run)
        
class DissipSourceOfEemAndEpare(DiagnosticScalarVariable):
    # 1/2*Mu*(Jpar/Nea)^2 * (Dn+Sn)
    def __init__(self, run=None):
        index_in_netcdf = 64
        title = "Eem+Epare"
        
        super().__init__(index_in_netcdf, run=run)
        
class DissipSourceOfEthi(DiagnosticScalarVariable):
    # 3/2*Tia*(Dn+Sn) + 3/2*Nea*(Dti+Sti)
    def __init__(self, run=None):
        index_in_netcdf = 65
        title = "Ethi"
        
        super().__init__(index_in_netcdf, run=run)
        
class NeutralsDensity(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 71
        title = "N Dens"
        
        super().__init__(index_in_netcdf, run=run)
    
    def update_normalisation_factor(self):
        self.normalisation_factor = self.normalisation.n0
        
class IonizationDensitySource(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 72
        title = "Iz src"
        
        super().__init__(index_in_netcdf, run=run)
        
class IonizationCooling(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 73
        title = "Iz cooling"
        
        super().__init__(index_in_netcdf, run=run)
        
class CXFrictionOnParallelIonVelocity(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 74
        title = "CX on Upar"
        
        super().__init__(index_in_netcdf, run=run)
        
class CXFrictionOnVorticity(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 75
        title = "CX on Vort"
        
        super().__init__(index_in_netcdf, run=run)
        
class DerivativeNeutralsDensity(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 76
        title = "d/dt  N Dens"
        
        super().__init__(index_in_netcdf, run=run)
        