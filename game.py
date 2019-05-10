import numpy as np
import tqdm
import random

from env import Env
from agent import Agent
from tools import *

class Game():
    def __init__(self,size,num_agents=1,max_life=100,num_teams=2,configs=None,viewrange=1):
        self.size = size
        self.env = Env(size,viewrange)
        self.agent_configs = {"num_agents":num_agents,"max_life":max_life,"viewrange":viewrange}
        self.live_agents = {}
        self.num_teams = num_teams
        if configs == None:
            self.createAgents()
            self.initialize()

    #getters
    def getNumTeams(self):
        return self.num_teams

    def getAgents(self):
        return self.live_agents
    #processing
    def createAgents(self):
        num_agents = self.agent_configs["num_agents"]
        max_life = self.agent_configs["max_life"]
        viewrange = self.agent_configs["viewrange"]
        for team in range(self.num_teams):
            c = 0
            while c < num_agents:
                agentId = "T{}Agent{}".format(team,c)
                c += 1
                agent = Agent(agentId,max_life,team,viewrange=viewrange)
                self.live_agents[agentId] = agent

    def initialize(self):
        l = list(self.live_agents.keys())
        random.shuffle(l)
        c = 0
        while c < len(l):
            agent = self.live_agents[l[c]]
            team = agent.getTeam()
            coord = (np.random.choice(self.size),int(np.random.uniform((team)*((self.size)//self.num_teams),(team+1)*(self.size//self.num_teams))))
            if not self.env.getCell(coord).getOccupied():
                self.env.place(coord,agent)
                c += 1

    def iter(self):
        l = list(self.live_agents.keys())
        random.shuffle(l)
        for agentId in l:
            agent = self.live_agents[agentId]
            if agent.isAlive():
                states, actions, coord_list = self.env.getStatesActions(agent)
                action = agent.train_policy(states,actions)
                self.env.step(agent,action,coord_list)
        agent_count, team_count = self.env.countAgents(self.num_teams)
        return self.env.encode(), self.env.__str__(),agent_count, team_count, self.serializeAgents()

    def playEpisodes(self,num_episodes,pyg=False):
        frames = [self.env.encode()]
        framestr = [self.env.__str__()]
        agent_counts = [self.env.countAgents(self.num_teams)]
        agents = [self.serializeAgents()]
        team_counts = [[self.agent_configs["num_agents"]]*self.num_teams]
        bar = tqdm.tqdm(np.arange(num_episodes))
        for i in bar:
            encoded, envstr, agent_count, team_count, serialized_agents = self.iter()
            frames.append(encoded)
            framestr.append(envstr)
            agents.append(serialized_agents)
            agent_counts.append(agent_count)
            team_counts.append(team_count)
            bar.set_description("Episode: {} with agent count {}".format(i,agent_count))
        # if pyg:
        #     playGrid(frames)
        # else:
        #     animate(framestr)
        return frames, framestr, agent_counts, team_counts, agents

    def serializeAgents(self):
        serialized = {}
        for agentId in self.live_agents.keys():
            agent = self.live_agents[agentId]
            serialized[agentId] = agent.serialize()
        return serialized

    def printEnv(self):
        print(self.env)

if __name__ == "__main__":
    game = Game(20,num_agents=1)
    frames = game.playEpisodes(100)
