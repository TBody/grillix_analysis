
class Something:

    def __init__(self):

        print("I waz here")
        print(f"{self}.__class__.__name__")
    

class SomethingElse(Something):
    pass


A = Something()

B = SomethingElse()