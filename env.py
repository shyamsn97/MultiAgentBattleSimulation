import numpy as np

from node import Node
class Env():
    def __init__(self,size,viewrange):
        self.size = size
        self.board = [[Node(0) for i in range(size)] for j in range(size)]

    #getters
    def getBoard(self):
        return self.board

    def getState(self,agent):
        r,c = agent.getPosition()
        team = agent.getTeam()
        identity = agent.getIdentity()
        viewrange = agent.getViewRange()
        state = np.zeros((3,1+viewrange*2,1+viewrange*2))
        for i in range(1 + viewrange*2):
            for j in range(1 + viewrange*2):
                coord = (r + (i-1),c + (j-1))
                if coord[0] >= 0 and coord[1] >= 0 and coord[0] < self.size and coord[1] < self.size:
                    #check if valid
                    node = self.getCell(coord)
                    if node.getOccupied():
                        state[0][i][j] = 1
                        agent = node.getAgent()
                        if agent.getTeam() != team:
                            state[2][i][j] = agent.getLife()
                        else:
                            state[1][i][j] = agent.getLife()
        return state.flatten()

    def getActions(self,agent):
        r,c = agent.getPosition()
        team = agent.getTeam()
        identity = agent.getIdentity()
        attackrange = 1 + agent.getAttackRange()*2
        moverange = 1 + agent.getMoveRange()*2
        moves = np.zeros((moverange,moverange))
        actions = np.zeros((attackrange,attackrange))
        coord_list = []
        for i in range(moverange):
            for j in range(moverange):
                coord = (r + (i-1),c + (j-1))
                if coord[0] == r and coord[1]:
                    coord_list.append(("pass",coord))
                    moves[i][j] = 1
                else:
                    coord_list.append(("move",coord))
                    if coord[0] >= 0 and coord[1] >= 0 and coord[0] < self.size and coord[1] < self.size:
                        #check if valid
                        node = self.getCell(coord)
                        if node.getOccupied() == False:
                            moves[i][j] = 1

        for i in range(attackrange):
            for j in range(attackrange):
                coord = (r + (i-1),c + (j-1))
                coord_list.append(("attack",coord))
                if coord[0] >= 0 and coord[1] >= 0 and coord[0] < self.size and coord[1] < self.size:
                    #check if valid
                    node = self.getCell(coord)
                    if node.getOccupied():
                        attacked_agent = node.getAgent()
                        if attacked_agent.getTeam() != team:
                            actions[i][j] = 1
        moves = moves.flatten()
        actions = actions.flatten()
        return np.concatenate((moves,actions)), coord_list



    #state and actions
    def getStatesActions(self,agent):
        states = self.getState(agent)
        moves, coord_list = self.getActions(agent)
        return states, moves , coord_list
    
    #processing
    def step(self,agent,action,coord_list):
        coord_action = coord_list[action]
        if coord_action[0] == "move":
            self.move(coord_action[1],agent)
        elif coord_action[0] == "attack":
            self.attack(coord_action[1],agent)
        elif coord_action[0] == "pass":
            pass
        # newcoord = action[1]
        # if action[0] == "move":
        #     self.move(newcoord,agent)
        # elif action[0] == "attack":
        #     self.attack(newcoord,agent)
        # originalPosition = agent.getPosition()
        # self.remove(originalPosition)
        # self.place(action,agent)

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
        if agent.deliverDamage(damage,attacked_agent) == False:
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


