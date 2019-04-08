import numpy as np

class Node():
    def __init__(self,identity=0):
        """
            indentity:
                0: clear
                1: occupied
        """
        self.identity = identity
    #getters
    def getIdentity(self):
        return self.identity

    #setters
    def setIdentity(self,value):
        self.identity = value

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.identity == other.getIdentity()

        elif isinstance(other,int):
            return self.identity == other

        return NotImplemented

    def __str__(self):
        return str(self.identity)

    def __int__(self):
        return self.identity
