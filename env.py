import numpy as np

from node import Node

class Env():
    def __init__(self,size,viewrange):
        self.size = size
        self.board = [[Node(0) for i in range(size)] for j in range(size)]

    #getters
    def getBoard(self):
        return self.board
    #processing
    def step(self,agent,action):
        originalPosition = agent.getPosition()
        self.remove(originalPosition)
        self.place(action,agent)

    def countAgents(self):
        c = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j].getOccupied():
                    c += 1
        return c

    def getMoves(self,agent):
        originalPosition = agent.getPosition()
        viewrange = agent.getViewRange()
        actions = np.zeros((1 + viewrange*2,1 + viewrange*2))
        #temporary, should be in matrix form, with a key to convert back
        r = originalPosition[0]
        c = originalPosition[1]
        valid = []
        for i in range(1 + viewrange*2):
            for j in range(1 + viewrange*2):
                coord = (r + (i-1),c + (j-1))
                if coord[0] >= 0 and coord[1] >= 0 and coord[0] < self.size and coord[1] < self.size:
                    #check if valid
                    if not self.getCell(coord).getOccupied():
                        valid.append(coord)
        return valid

    def remove(self,coord):
        self.getCell(coord).remove()

    def place(self,coord,agent):
        agent.setPosition(coord)
        self.getCell(coord).occupy(agent)
        
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

