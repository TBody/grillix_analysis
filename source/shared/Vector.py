# Based on https://codereview.stackexchange.com/questions/151205/2d-vector-class
from source import np

class Vector(object):
    
    def __init__(self, R, Z, phi):
        self.data = np.array(R, phi, Z)

    # def __add__(self, other):
    #     return Vector(self.data + other)

    # def __radd__(self, other):
    #     return Vector(other + self.data)

    # def __sub__(self, other):
    #     return Vector(self.data - other)

    # def __rsub__(self, other):
    #     return Vector(other - self.data)

    # def __mul__(self, other):
    #     return Vector(self.data * other)

    # def __rmul__(self, other):
    #     return Vector(other * self.data)

    # def __div__(self, other):
    #     return Vector(self.data / other)

    # def __rdiv__(self, other):
    #     return Vector(other / self.data)

    # def __neg__(self):
    #     return Vector(-self.data)

    # def __pos__(self):
    #     return Vector(+self.data)

    # def __eQuantity_(self, other):
    #     return np.array_equal(self.data, other.data)

    # def __ne__(self, other):
    #     return not self.__eQuantity_(other)

    # def __lt__(self, other):
    #     return self.square_length() < other.square_length()

    # def __le__(self, other):
    #     return self.square_length() <= other.square_length()

    # def __gt__(self, other):
    #     return self.square_length() > other.square_length()

    # def __ge__(self, other):
    #     return self.square_length() >= other.square_length()

    # def __repr__(self):
    #     return self.__str__()

    # def __str__(self):
    #     return np.array_str(self.data)

    # def ceil(self):
    #     return Vector(np.ceil(self.data))

    # def floor(self):
    #     return Vector(np.floor(self.data))

    # def get_data(self):
    #     return self.data

    # def inverse(self):
    #     return Vector(1.0/self.data)

    # def length(self):
    #     return float(np.linalg.norm(self.data))

    # def normalize(self):
    #     length = self.length()
    #     if length == 0.0:
    #         return Vector(np.zeros(self.data.shape()))
    #     return Vector(self.data/length)

    # @classmethod
    # def distance(cls, a, b):
    #     c = b - a
    #     return c.length()

    # @classmethod
    # def dot(cls, a, b):
    #     return Vector(np.dot(a.data, b.data))

    # @classmethod
    # def square_distance(cls, a, b):
    #     c = b - a
    #     return c.square_length()
