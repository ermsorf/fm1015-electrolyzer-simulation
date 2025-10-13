# run in home folder if running tests 
if __name__ == "__main__": import os; import sys; sys.path.append(os.getcwd())
from typing import Callable
from operator import add,sub,mul, truediv

def operate(operator, self: 'Mols', other: 'Mols'):
    """
    Generates a function to
    compute A[operator]B
    for two species
    (e.g A+B, A-B, A*B, A/B)
    """
    out = Mols()
    for attribute in other.species.keys():
        if other.species[attribute] == 0: out[attribute] = 0; continue
        out[attribute] = operator(self.species[attribute], other.species[attribute])
    return out

class Mols():
    def __init__(self, LH2O = 0.0, LH2 = 0.0, LO2 = 0.0, GH2O = 0.0, GH2 = 0.0, GO2 = 0.0):
        self.species = {"LH2O": LH2O, "LO2": LH2, "LH2": LO2, "GH2O": GH2O, "GO2": GH2, "GH2": GO2}
        return 
    # getting/setting
    def __getitem__(self, name):
        return self.species[name]
    def __setitem__(self, species, value):
        self.species[species] = value
    def __iter__(self):
        return iter(self.species.values())
    # Math 
    def __add__(self, other: 'Mols'):
        return operate(add, self, other)
    def __sub__(self, other: 'Mols'):
        return operate(sub, self, other)
    def __mul__(self, other):
        # Handle scalar multiplication
        if isinstance(other, (int, float)):
            out = Mols()
            for key in self.species.keys():
                out[key] = self.species[key] * other
            return out
        # Handle Mols * Mols
        return operate(mul, self, other)
    def __rmul__(self, other):
        # Handle reverse multiplication (scalar * Mols)
        return self.__mul__(other)
    def __truediv__(self, other):
        # Handle scalar division
        if isinstance(other, (int, float)):
            out = Mols()
            for key in self.species.keys():
                out[key] = self.species[key] / other
            return out
        # Handle Mols / Mols
        return operate(truediv, self, other)
    def __str__(self):
        return (f' - LH2O: {self.species["LH2O"]}\n'
               +f' - LH2: {self.species["LH2"]}\n'
               +f' - LO2: {self.species["LO2"]}\n'
               +f' - GH2O: {self.species["GH2O"]}\n'
               +f' - GH2: {self.species["GH2"]}\n'
               +f' - GO2: {self.species["GO2"]}\n')
    # dict lookups
    @staticmethod
    def keys():
        return ("LH2O", "LH2", "LO2", "GH2O", "GH2", "GO2")
    def values(self):
        return [self.species[key] for key in self.keys()]
    
    def get_sums(self):
        sp = self.species
        return{"H2O": sp["LH2O"] + sp["GH2O"],
                "H2": sp["LH2"] + sp["GH2"],
                "O2": sp["LO2"] + sp["GO2"]
                }


if __name__ == "__main__":
    x = Mols(LH2 = 1, LO2 = 1, LH2O = 1, GH2 = 1, GO2= 1, GH2O = 1)
    y = Mols(LH2 = 2, LO2 = 2, LH2O = 2, GH2 = 2, GO2= 2, GH2O = 2)
    z = Mols()

    print( x + y + z ) 
    print( x - y - z ) 
    print( x * y * z ) 
    print( x / y / z )  
        