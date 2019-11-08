class Node:
    def __init__(self, identity=0):
        """
            indentity:
                0: clear
                1 to n: other terrain
        """
        self.identity = identity
        self.isOccupied = False
        self.agent = None

    # getters
    def getIdentity(self):
        return self.identity

    def getAgent(self):
        return self.agent

    def getOccupied(self):
        return self.isOccupied

    # setters
    def setIdentity(self, value):
        self.identity = value

    def remove(self):
        self.isOccupied = False
        self.agent = None

    def occupy(self, agent):
        self.isOccupied = True
        self.agent = agent

    # comparison functions
    def __eq__(self, other):
        if isinstance(other, Node):
            return self.identity == other.getIdentity()

        elif isinstance(other, int):
            return self.identity == other

        return False

    def __str__(self):
        return str(self.identity)

    def __int__(self):
        return self.identity
