import numpy as np
from node import Node

class State():
    def __init__(self,agent,board_size,flatten=True):
        self.life = agent.getLife()
        self.viewrange = agent.getViewRange()
        self.moverange =  1 + agent.getMoveRange()*2
        self.attackrange = 1 + agent.getAttackRange()*2
        self.team = agent.getTeam()
        self.identity = agent.getIdentity()
        #flatten determines whether to flatten 
        self.flatten = flatten 
        self.board_size = board_size


