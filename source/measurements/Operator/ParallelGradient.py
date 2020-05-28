from . import Operator
from source import np
from source.shared.CSRMatrix import CSRMatrix
from ..WrappedArray import ScalarArray

class ParallelGradient(Operator):
    # evaluates parallel gradient, result on staggered grid
    # du =  (VB)^(-1) * qmap * uf
    #
    # VB is magnetic field integrated over flux box volume
    # qmap is map matrix
    #
    # Give vector_k at plane k
    # vector_next_plane at k+1
    # Returns gradient at k+1/2

    # From grid values, interpolate to find the values at points which intersected by parallel trace
    # Execute qmap * uf
    
    def __init__(self, run=None):
        super().__init__(run=run)
        self.title = "Par. Grad."

    def set_run(self):

        self.f2s_map_forward = CSRMatrix(self.run.directory.f2s_map_forward_file, self.run.grid)
        self.f2s_map_reverse = CSRMatrix(self.run.directory.f2s_map_reverse_file, self.run.grid)
        self.map_metadata = self.run.directory.map_metadata_file
        self.npol = self.run.parameters["params_grid"]["npol"]

        self.forward_in_grid = self.map_metadata['forward_in_grid'][:]
        self.backward_in_grid = self.map_metadata['backward_in_grid'][:]

        # # Distance to k+1/2
        self.L_half_forward = self.map_metadata['map_metadata'][0,:]
        # # Distance to k-1/2
        self.L_half_backward = self.map_metadata['map_metadata'][1,:]
        # # Flux box volume
        self.flux_box_volume = self.map_metadata['map_metadata'][2,:]
        # # Distance to k+1
        self.L_full_forward = self.map_metadata['map_metadata'][3,:]
        # # Distance to k-1
        self.L_full_backward = self.map_metadata['map_metadata'][4,:]
    
    def __call__(self, values, units):
        
        # Assert that all planes have been given
        assert(values.shape[1] == self.npol)
        # Assert that the number of points matches the size of the csr matrices (which must be square)
        assert(np.all(values.shape[2]==np.array(self.f2s_map_forward.get_shape())))
        assert(np.all(values.shape[2]==np.array(self.f2s_map_reverse.get_shape())))
        # Make sure that values is not a vector
        assert(not(values.is_vector))
        
        Btor, _ = self.run.equilibrium.Btor()
        fieldline_length = self.normalisation.R0 * Btor * (self.L_half_forward + self.L_half_backward)
        
        # The one-liner code is admittedly confusing. To test against an explicit loop, uncomment the following lines and
        # the assert block at the end
        # z_stag_forward_v0 = np.zeros_like(values)
        # z_stag_reverse_v0 = np.zeros_like(values)
        # gradient_stag_v0 = np.zeros_like(values)
        
        # for time_index in range(values.shape[0]):
        #     for plane_index in range(values.shape[1]):
        #         next_plane_index = np.mod(plane_index+1, values.shape[1])
        #         z_stag_forward_v0[time_index, plane_index, :] = self.f2s_map_forward(values[time_index, next_plane_index, :])
        #         z_stag_reverse_v0[time_index, plane_index, :] = self.f2s_map_reverse(values[time_index, plane_index, :])
                
        #         gradient_stag_v0[time_index, plane_index, :] = (
        #               z_stag_forward_v0[time_index, plane_index, :] 
        #             - z_stag_reverse_v0[time_index, plane_index, :])/fieldline_length
        # IMPORTANT: to get data on the next plane, you should use np.roll(array, shift=-1, axis=1) where axis=1 is to get the planes dimension
        # The shift=-1 is confusing, but you can test that it's doing the right thing by trying
        # next_plane = np.roll(np.arange(n_planes), shift=-1)
        # Then, next_plane[i] will be [i+1]
        
        z_stag_forward = np.apply_along_axis(self.f2s_map_forward, axis=2, arr=self.find_neighbouring_plane(values))
        z_stag_reverse = np.apply_along_axis(self.f2s_map_reverse, axis=2, arr=values)
        
        gradient_stag = (z_stag_forward - z_stag_reverse)*units/fieldline_length
        units *= 1/self.run.normalisation.R0
        
        # assert(np.allclose(z_stag_reverse, z_stag_reverse_v0))
        # assert(np.allclose(z_stag_forward, z_stag_forward_v0))
        # assert(np.allclose(gradient_stag, gradient_stag_v0))
        
        return ScalarArray((gradient_stag/units).to('').magnitude), units
        