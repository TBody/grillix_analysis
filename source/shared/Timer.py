import time

class Timer:
    
    def __init__(self):
        self.time_start = time.time()
    
    def __str__(self):
        return f"Run time: {time.time() - self.time_start:3.2f}s"


