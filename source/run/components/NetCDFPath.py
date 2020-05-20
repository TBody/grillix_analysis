from source import Path, Dataset

class NetCDFPath():
    # Intuitively, would make a subclass of Path, but there is an issue with
    # inheritance of pathlib.Path
    
    def __init__(self, filepath):
        self.filepath = Path(filepath)
        assert(self.filepath.exists)
        
        self.is_open = False
        self.dataset = []
    
    def exists(self):
        return self.filepath.exists()
    
    def __str__(self):
        if self.is_open:
            return str(self.dataset)
        else:
            return str(self.filepath)
    
    def open(self):
        
        if not(self.is_open):
            self.dataset = Dataset(self.filepath)
            self.is_open = True
        
        return self.dataset
    
    def close(self):
        
        self.dataset.close()
    
    def __getitem__(self, key):
        
        if not(self.is_open):
            self.open()
        return self.dataset[key]
    
    def __getattr__(self, attr):
    
        if not(attr is 'dataset'):
            if not(self.is_open):
                self.open()
            return getattr(self.dataset, attr)
        else:
            return self.dataset