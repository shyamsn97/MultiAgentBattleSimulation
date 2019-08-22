import numpy as np
import random

from node import Node
from Board import Board

class Env():
	def __init__(self,size,num_teams):
		self.size = size
		self.board = Board(size)
		self.num_teams = num_teams

	#getters
	def getBoard(self):
		return self.board
	
	#processing
	def flushAgents(self,agent_dict):
		for agent in agent_dict:
			agent_dict[agent].flush()

	def initialize(self,agent_dict):
		self.flushAgents(agent_dict)
		self.board = Board(self.size)
		l = list(agent_dict.keys())
		random.shuffle(l)
		size = self.board.size
		c = 0
		while c < len(l):
			agent = agent_dict[l[c]]
			team = agent.getTeam()
			coord = (np.random.choice(size),int(np.random.uniform((team)*((size)//self.num_teams),
																(team+1)*(size//self.num_teams))))
			if not self.board.getCell(coord).getOccupied():
				self.board.place(coord,agent)
				c += 1

	def step(self,agent,action,coord_list):
		coord_action = coord_list[action]
		if coord_action[0] == "move":
			self.board.move(coord_action[1],agent)
		elif coord_action[0] == "attack":
			self.board.attack(coord_action[1],agent)
		elif coord_action[0] == "pass":
			pass

	def countAgents(self,num_teams):
		c, teamCount = self.board.countAgents(num_teams)
		return c, teamCount

	def getStatesActions(self,agent):
		return self.board.getStatesActions(agent)

	def encode(self):
		return self.board.encode()

	def __str__(self):
		return self.board.__str__()
	



