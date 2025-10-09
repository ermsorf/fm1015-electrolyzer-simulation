from typing import Callable
from operator import add,sub,mul, truediv

def generate_operator(operator: Callable):
    """
    Generates a function to
    compute A[operator]B
    for two species
    (e.g A+B, A-B, A*B, A/B)
    """
    def operate(self: 'Moles', other: 'Moles'):
        out = Moles()
        for attribute in other.species.keys():
            out[attribute] = operator(self.species[attribute], other.species[attribute])
        return out
    return operate

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
        op = generate_operator(add)
        return op(self, other)
    def __sub__(self, other: 'Moles'):
        op = generate_operator(sub)
        return op(self, other)
    def __mul__(self, other: 'Moles'):
        op = generate_operator(mul)
        return op(self, other)
    def __div__(self, other: 'Moles'):
        op = generate_operator(truediv)
        return op(self, other)
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