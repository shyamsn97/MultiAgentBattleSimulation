import numpy as np

from node import Node

class Board():
    def __init__(self,size):
        self.size = size
        self.board = [[Node(0) for i in range(size)] for j in range(size)]

    def getActions(self,agent):
        """
            action key:
                # [move_left,move_right,move_up,move_down,attack_left,attack_right,attack_up,attack_down]
        """
        r,c = agent.getPosition()

    def getMoves(self,coord):
        actions = np.zeros((3,3))
        #temporary
        r = coord[0]
        c = coord[1]
        valid = []
        for i in range(3):
            for j in range(3):
                coord = (r + (i-1),c + (j-1))
                if coord[0] >= 0 and coord[1] >= 0 and coord[0] < self.size and coord[1] < self.size:
                    if self.board[coord[0]][coord[1]] == 0:
                        valid.append((coord[0],coord[1]))
        return valid

    def place(self,value,coord):
        r = coord[0]
        c = coord[1]
        self.board[r][c].setIdentity(value)
        
    def getCell(self,coord):
        r = coord[0]
        c = coord[1]
        return self.board[r][c]

    def encode(self):
        board = [[0]*self.size for i in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                board[i][j] = int(self.board[i][j])
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
