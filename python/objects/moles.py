# run in home folder if running tests 
if __name__ == "__main__": import os; import sys; sys.path.append(os.getcwd())
from typing import Callable
from operator import add,sub,mul, truediv

def operate(operator, self: 'Moles', other: 'Moles'):
    """
    Generates a function to
    compute A[operator]B
    for two species
    (e.g A+B, A-B, A*B, A/B)
    """
    out = Moles()
    for attribute in other.species.keys():
        out[attribute] = operator(self.species[attribute], other.species[attribute])
    return out

class Moles():
    def __init__(self, H2O = 0.0, O2 = 0.0, H2 = 0.0):
        self.species = {"H2O": H2O, "O2": O2, "H2": H2}
        return 
    # getting/setting
    def __getitem__(self, name):
        return self.species[name]
    def __setitem__(self, species, value):
        self.species[species] = value
    def __iter__(self):
        return iter(self.species.values())
    # Math 
    def __add__(self, other: 'Moles'):
        return operate(add, self, other)
    def __sub__(self, other: 'Moles'):
        return operate(sub, self, other)
    def __mul__(self, other: 'Moles'):
        return operate(mul, self, other)
    def __div__(self, other: 'Moles'):
        return operate(truediv, self, other)
    def __str__(self):
        return (f' - H2O: {self.species["H2O"]}\n'
               +f' - O2: {self.species["O2"]}\n'
               +f' - H2: {self.species["H2"]}')
    # dict lookups
    @staticmethod
    def keys():
        return ("H2O", "H2", "O2")
    def values(self):
        return [self.species[key] for key in self.keys()]