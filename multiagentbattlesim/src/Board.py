import numpy as np

from .Node import Node
from .State import State

class Board():
	def __init__(self,size):
		self.size = size
		self.board = [[Node(0) for i in range(size)] for j in range(size)]

	def getCell(cell,coord):
		return self.board[coord[0]][coord[1]]

	def remove(self,coord):
		self.board[coord[0]][coord[1]].remove()

	def place(self,coord,agent):
		originalPosition = agent.getPosition()
		if originalPosition != None:
			self.remove(originalPosition)
		self.board[coord[0]][coord[1]].occupy(agent)
		agent.updateLocation(coord)
		return agent.getLivingReward()

	def move(self,newcoord,agent):
		originalPosition = agent.getPosition()
		self.remove(originalPosition)
		return self.place(newcoord,agent)

	def attack(self,coord,agent):
		damage = agent.getDamage()
		attacked_node = self.getCell(coord)
		attacked_agent = attacked_node.getAgent()
		reward, dead =  agent.deliverDamage(damage,attacked_agent)
		if dead == False:
			attacked_node.remove()
		return reward


	def getCell(self,coord):
		r = coord[0]
		c = coord[1]
		return self.board[r][c]


	def countAgents(self,numTeams):
		teamCount = [0]*numTeams
		c = 0
		for i in range(len(self.board)):
			for j in range(len(self.board[0])):
				node = self.getCell((i,j))
				if node.getOccupied():
					agent = node.getAgent()
					if agent.isAlive():
						c += 1
						teamCount[agent.getTeam()] += 1
		return c, teamCount
	'''
		States and actions
	'''
	def getState(self,agent,flatten=True):
		r,c = agent.getPosition()
		agentState = State(agent,self.size,flatten)
		state = np.zeros((3,1+agentState.viewrange*2,1+agentState.viewrange*2))
		for i in range(1 + agentState.viewrange*2):
			for j in range(1 + agentState.viewrange*2):
				coord = (r + (i-1),c + (j-1))
				if coord[0] >= 0 and coord[1] >= 0 and coord[0] < self.size and coord[1] < self.size:
					#check if valid
					node = self.getCell(coord)
					if node.getOccupied():
						state[0][i][j] = 1
						agent = node.getAgent()
						if agent.getTeam() != agentState.team:
							state[2][i][j] = agent.getLife()
						else:
							state[1][i][j] = agent.getLife()
		if flatten:
			return state.flatten()
		return state

	def getActions(self,agent,agentState=None,flatten=True):
		r,c = agent.getPosition()
		if agentState == None:
			agentState = State(agent,self.size,flatten)
		moves = np.zeros((agentState.moverange,agentState.moverange))
		actions = np.zeros((agentState.attackrange,agentState.attackrange))
		coord_list = []
		coord_dict = {}
		for i in range(agentState.moverange):
			for j in range(agentState.moverange):
				coord = (r + (i-1),c + (j-1))
				if coord[0] == r and coord[1] == c:
					coord_list.append(("pass",coord))
					moves[i][j] = 1
				else:
					coord_list.append(("move",coord))
					if coord[0] >= 0 and coord[1] >= 0 and coord[0] < self.size and coord[1] < self.size:
						#check if valid
						node = self.getCell(coord)
						if node.getOccupied() == False:
							moves[i][j] = 1

		for i in range(agentState.attackrange):
			for j in range(agentState.attackrange):
				coord = (r + (i-1),c + (j-1))
				coord_list.append(("pass",coord))
				if coord[0] >= 0 and coord[1] >= 0 and coord[0] < self.size and coord[1] < self.size:
					#check if valid
					node = self.getCell(coord)
					if node.getOccupied():
						attacked_agent = node.getAgent()
						if attacked_agent.getTeam() != agentState.team:
							actions[i][j] = 1
							coord_list[-1] = (("attack",coord))
		if flatten:
			moves = moves.flatten()
			actions = actions.flatten()
		valid_actions = np.concatenate((moves,actions))
		return valid_actions, coord_list

	#state and actions
	def getStatesActions(self,agent):
		states = self.getState(agent)
		valid_actions, coord_list = self.getActions(agent)
		return states, valid_actions, coord_list


	#encoding 
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



