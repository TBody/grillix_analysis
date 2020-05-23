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
        
        return values.shape_poloidal()

class Time(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 1
        
        super().__init__(index_in_netcdf, run=run)
    
    @property
    def normalisation_factor(self):
        return self.normalisation.tau_0

class Timestep(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 2
        
        super().__init__(index_in_netcdf, run=run)
    
    @property
    def normalisation_factor(self):
        return self.normalisation.tau_0

class AverageDensity(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 11
        super().__init__(index_in_netcdf, title="Density", run=run)
    
    @property
    def normalisation_factor(self):
        return self.normalisation.n0

class AverageElectronTemperature(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 12
        super().__init__(index_in_netcdf, title="ETemp", run=run)
    
    @property
    def normalisation_factor(self):
        return self.normalisation.Te0

class AverageIonTemperature(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 13
        super().__init__(index_in_netcdf, title="ITemp", run=run)
    
    @property
    def normalisation_factor(self):
        return self.normalisation.Ti0

class AverageScalarPotential(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 14
        super().__init__(index_in_netcdf, title="Phi", run=run)
    
    @property
    def normalisation_factor(self):
        return (self.normalisation.Te0/self.normalisation.electron_charge).to("kilovolt")

class AverageVorticity(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 15
        super().__init__(index_in_netcdf, title="Vort", run=run)
    
    @property
    def normalisation_factor(self):
        return (
            self.normalisation.Mi * self.normalisation.n0 * self.normalisation.Te0
            /(self.normalisation.electron_charge * self.normalisation.rho_s0**2 * self.normalisation.B0**2 )
        ).to('coulomb/meter**3')

class AverageParallelCurrent(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 16
        super().__init__(index_in_netcdf, title="Jpar", run=run)
    
    @property
    def normalisation_factor(self):
        return (self.normalisation.c_s0 * self.normalisation.electron_charge * self.normalisation.n0).to(
            'kiloampere*meter**-2'
        )

class AverageParallelIonVelocity(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 17
        super().__init__(index_in_netcdf, title="Upar", run=run)
    
    @property
    def normalisation_factor(self):
        return self.normalisation.c_s0.to('kilometers/second')

class AverageParallelVectorPotential(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 18
        super().__init__(index_in_netcdf, title="Apar", run=run)
    
    def update_normalisation_factor(self):
    
        self.normalisation_factor = self.normalisation.beta_0 * self.normalisation.B0 * self.normalisation.rho_s0

class AveragePerpendicularKineticEnergy(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 21
        super().__init__(index_in_netcdf, title="K.E. perp", run=run)
        
class AverageParallelKineticEnergy(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 22
        super().__init__(index_in_netcdf, title="K.E. par", run=run)
        
class AverageElectronThermalEnergy(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 23
        super().__init__(index_in_netcdf, title="T.E. e", run=run)

class AverageIonThermalEnergy(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 24
        super().__init__(index_in_netcdf, title="T.E. i", run=run)
        
class AverageMagneticEnergy(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 25
        super().__init__(index_in_netcdf, title="Mag.E.", run=run)
        
class AverageParallelKineticElectronEnergy(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 26
        super().__init__(index_in_netcdf, title="K.E. par e", run=run)
        
class DerivativeDensity(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 31
        super().__init__(index_in_netcdf, title="d/dt Density", run=run)
        
class DerivativePerpendicularKineticEnergy(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 32
        super().__init__(index_in_netcdf, title="d/dt K.E. perp", run=run)

class DerivativeParallelKineticEnergy(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 33
        super().__init__(index_in_netcdf, title="d/dt K.E. par", run=run)

class DerivativeElectronThermalEnergy(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 34
        super().__init__(index_in_netcdf, title="d/dt T.E. e", run=run)

class DerivativeIonThermalEnergy(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 35
        super().__init__(index_in_netcdf, title="d/dt T.E. i", run=run)

class DerivativeMagneticEnergy(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 36
        super().__init__(index_in_netcdf, title="d/dt Mag.E.", run=run)

class DerivativeParallelKineticElectronEnergy(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 37
        super().__init__(index_in_netcdf, title="d/dt K.E. par e", run=run)

class ParticleSource(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 41
        super().__init__(index_in_netcdf, title="Source", run=run)
        
class ParticleSink(DiagnosticScalarVariable):
    # Particle Sink (due to diffusion/dissipation at boundaries)

    def __init__(self, run=None):
        index_in_netcdf = 42
        super().__init__(index_in_netcdf, title="Sink", run=run)
        
class TransferTermOfEperpAndEthe(DiagnosticScalarVariable):
    # "Jpar*Grad_par(Pot)"
    def __init__(self, run=None):
        index_in_netcdf = 51
        super().__init__(index_in_netcdf, title="E perp -> Ethe", run=run)
            
class TransferTermOfEperpFromTe(DiagnosticScalarVariable):
    # Nea*Tea*Div(V_e)
    def __init__(self, run=None):
        index_in_netcdf = 52
        super().__init__(index_in_netcdf, title="Te -> E perp ", run=run)
        
class TransferTermOfEparFromTe(DiagnosticScalarVariable):
    # -Upar*Grad_par(Nea*Tea)>
    def __init__(self, run=None):
        index_in_netcdf = 53
        super().__init__(index_in_netcdf, title="Te -> E par", run=run)
        
class TransferTermOfEthe1(DiagnosticScalarVariable):
    # Vpar*Grad_par(Nea*Tea)>
    def __init__(self, run=None):
        index_in_netcdf = 54
        super().__init__(index_in_netcdf, title="E the 1", run=run)
            
class TransferTermOfEthe2(DiagnosticScalarVariable):
    # Etapar/Jpar^2/(Tea^(3/2))>
    def __init__(self, run=None):
        index_in_netcdf = 55
        super().__init__(index_in_netcdf, title="E the 2", run=run)
        
class TransferTermOfEthe3(DiagnosticScalarVariable):
    # -0.71*Jpar*Grad_par(Tea)
    def __init__(self, run=None):
        index_in_netcdf = 56
        super().__init__(index_in_netcdf, title="E the 3", run=run)
        
class TransferTermOfEperpFromTi(DiagnosticScalarVariable):
    # Nea*Tia*Div(V_e)
    def __init__(self, run=None):
        index_in_netcdf = 57
        super().__init__(index_in_netcdf, title="Ti -> E perp", run=run)
        
class TransferTermOfEparFromTi(DiagnosticScalarVariable):
    # -Upar*Grad_par(Nea*Tia)
    def __init__(self, run=None):
        index_in_netcdf = 58
        super().__init__(index_in_netcdf, title="Ti -> E par", run=run)
        
class DissipSourceOfEperp(DiagnosticScalarVariable):
    # - Pot*Dw + (1-Bsq)>*|Nabla_perp(Pot)|^2 / (2b^2) * (Dn+Sn-Dw)
    def __init__(self, run=None):
        index_in_netcdf = 61
        super().__init__(index_in_netcdf, title="Eperp", run=run)
        
class DissipSourceOfEpar(DiagnosticScalarVariable):
    # Nea*Upar*Su + Nea*Upar*Du< + >Upar^2/2*(Dn+Sn-Dw)
    def __init__(self, run=None):
        index_in_netcdf = 62
        super().__init__(index_in_netcdf, title="Epar", run=run)
        
class DissipSourceOfEthe(DiagnosticScalarVariable):
    # 3/2*Tea*(Dn+Sn) + 3/2*Nea*(Dte+Ste)
    def __init__(self, run=None):
        index_in_netcdf = 63
        super().__init__(index_in_netcdf, title="Ethe", run=run)
        
class DissipSourceOfEemAndEpare(DiagnosticScalarVariable):
    # 1/2*Mu*(Jpar/Nea)^2 * (Dn+Sn)
    def __init__(self, run=None):
        index_in_netcdf = 64
        super().__init__(index_in_netcdf, title="Eem+Epare", run=run)
        
class DissipSourceOfEthi(DiagnosticScalarVariable):
    # 3/2*Tia*(Dn+Sn) + 3/2*Nea*(Dti+Sti)
    def __init__(self, run=None):
        index_in_netcdf = 65
        super().__init__(index_in_netcdf, title="Ethi", run=run)
        
class NeutralsDensity(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 71
        super().__init__(index_in_netcdf, title="N Dens", run=run)
    
    @property
    def normalisation_factor(self):
        return self.normalisation.n0
        
class IonizationDensitySource(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 72
        super().__init__(index_in_netcdf, title="Iz src", run=run)
        
class IonizationCooling(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 73
        super().__init__(index_in_netcdf, title="Iz cooling", run=run)
        
class CXFrictionOnParallelIonVelocity(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 74
        super().__init__(index_in_netcdf, title="CX on Upar", run=run)
        
class CXFrictionOnVorticity(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 75
        super().__init__(index_in_netcdf, title="CX on Vort", run=run)
        
class DerivativeNeutralsDensity(DiagnosticScalarVariable):

    def __init__(self, run=None):
        index_in_netcdf = 76
        super().__init__(index_in_netcdf, title="d/dt  N Dens", run=run)
        