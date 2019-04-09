import numpy as np

from node import Node

class Env():
    def __init__(self,size,viewrange):
        self.size = size
        self.board = [[Node(0) for i in range(size)] for j in range(size)]

    #getters
    def getBoard(self):
        return self.board

    #state and actions
    def getMoves(self,agent):
        originalPosition = agent.getPosition()
        team = agent.getTeam()
        identity = agent.getIdentity()
        viewrange = agent.getViewRange()
        attackrange = agent.getAttackRange()
        moves = np.zeros((1 + viewrange*2,1 + viewrange*2))
        actions = np.zeros((1 + attackrange*2,1 + attackrange*2))
        #temporary, should be in matrix form, with a key to convert back
        r = originalPosition[0]
        c = originalPosition[1]
        valid = []
        for i in range(1 + viewrange*2):
            for j in range(1 + viewrange*2):
                coord = (r + (i-1),c + (j-1))
                if coord[0] >= 0 and coord[1] >= 0 and coord[0] < self.size and coord[1] < self.size:
                    #check if valid
                    node = self.getCell(coord)
                    if not node.getOccupied():
                        valid.append(("move",coord))

        for i in range(1 + attackrange*2):
            for j in range(1 + attackrange*2):
                coord = (r + (i-1),c + (j-1))
                if coord[0] >= 0 and coord[1] >= 0 and coord[0] < self.size and coord[1] < self.size:
                    #check if valid
                    node = self.getCell(coord)
                    if node.getOccupied():
                        agent = node.getAgent()
                        if agent.getTeam() != team:
                            valid.append(("attack",coord))
        return valid
    #processing
    def step(self,agent,action):
        newcoord = action[1]
        if action[0] == "move":
            self.move(newcoord,agent)
        elif action[0] == "attack":
            self.attack(newcoord,agent)
        # originalPosition = agent.getPosition()
        # self.remove(originalPosition)
        # self.place(action,agent)

    def countAgents(self):
        c = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                node = self.getCell((i,j))
                if node.getOccupied():
                    if node.getAgent().isAlive():
                        c += 1
        return c

    def remove(self,coord):
        self.getCell(coord).remove()

    def place(self,coord,agent):
        agent.setPosition(coord)
        self.getCell(coord).occupy(agent)
    
    def move(self,newcoord,agent):
        originalPosition = agent.getPosition()
        self.remove(originalPosition)
        self.place(newcoord,agent)

    def attack(self,coord,agent):
        damage = agent.getDamage()
        attacked_node = self.getCell(coord)
        attacked_agent = attacked_node.getAgent()
        if attacked_agent.processDamage(damage) == False:
            attacked_node.remove()

    def getCell(self,coord):
        r = coord[0]
        c = coord[1]
        return self.board[r][c]

    def encode(self):
        board = [[0]*self.size for i in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                node = self.getCell((i,j))
                board[i][j] = int(node)
                if node.getOccupied():
                    agent = node.getAgent()
                    if agent.isAlive():
                        board[i][j] = agent.getTeam() + 1
        return board

    def __str__(self):
        out = ""
        s = "-"*(self.size*4) + "-" + "\n"
        for i in range(self.size):
            s += "|"
            for j in range(self.size):
                s += " " + str(self.board[i][j]) + " |"
            s += "\n" + "="*(self.size*4) + "=" + '\n'
        return s


