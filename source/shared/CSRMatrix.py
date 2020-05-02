from scipy.sparse import csr_matrix
from source import np, plt

class CSRMatrix(csr_matrix):

    def __init__(self, netcdf_file, grid):
        
        # Read in the data values -- see https://en.wikipedia.org/wiki/Sparse_matrix#Compressed_sparse_row_(CSR,_CRS_or_Yale_format) for reference of terminology
        # N.b. returns as a masked array -- want to use .filled() to convert to standard numpy array
        A = netcdf_file.variables['val'][:].filled(fill_value=np.NaN)
        IA = netcdf_file.variables['i'][:].filled(fill_value=np.NaN)
        JA = netcdf_file.variables['j'][:].filled(fill_value=np.NaN)

        # Appears that 1-indexing was used -- need to shift back to 0-indexing to use
        # python csr_matrix form
        IA = IA - 1
        JA = JA - 1

        # Construct the csr matrix according to csr_matrix((data, indices, indptr))
        # Note the double brackets
        # See https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csr_matrix.html
        # 
        # For clarity, super().__init__(*args) calls scipy.sparse.csr_matrix.__init__(*args)
        super().__init__((A, JA, IA), shape=(grid.size, grid.size))
    
    def __str__(self):
        return f"CSR matrix of shape {self.get_shape()} with {self.count_nonzero()} non-zero elements ({100*self.count_nonzero()/np.prod(self.get_shape()):4.3f}% filled)"
    
    def spy(self):
        
        plt.figure()
        plt.spy(self)
        plt.show()
    
    def __call__(self, z):
        return self.dot(z)