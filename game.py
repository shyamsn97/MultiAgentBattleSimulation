import numpy as np
import tqdm

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
            self.initialize()

    #getters
    def getNumTeams(self):
        return self.num_teams

    def getAgents(self):
        return self.live_agents
    #processing
    def initialize(self):
        num_agents = self.agent_configs["num_agents"]
        max_life = self.agent_configs["max_life"]
        viewrange = self.agent_configs["viewrange"]
        for team in range(self.num_teams):
            c = 0
            while c < num_agents:
                coord = (np.random.choice(self.size),np.random.choice(self.size))
                if not self.env.getCell(coord).getOccupied():
                    agentId = "T{}Agent{}".format(team,c)
                    c += 1
                    agent = Agent(agentId,coord,max_life,team,viewrange=viewrange)
                    self.env.place(coord,agent)
                    self.live_agents[agentId] = agent

    def iter(self):
        for agentId in self.live_agents.keys():
            agent = self.live_agents[agentId]
            if agent.isAlive():
                actions = self.env.getMoves(agent)
                action = agent.train_policy(actions)
                self.env.step(agent,action)

        return self.env.encode(), self.env.__str__(), self.env.countAgents(), self.serializeAgents()

    def playEpisodes(self,num_episodes,pyg=False):
        frames = [self.env.encode()]
        framestr = [self.env.__str__()]
        counts = [self.env.countAgents()]
        agents = [self.serializeAgents()]
        bar = tqdm.tqdm(np.arange(num_episodes))
        for i in bar:
            encoded, envstr, count, serialized_agents = self.iter()
            frames.append(encoded)
            framestr.append(envstr)
            agents.append(serialized_agents)
            counts.append(count)
            bar.set_description("Episode: {} with count {}".format(i,count))
        # if pyg:
        #     playGrid(frames)
        # else:
        #     animate(framestr)
        return frames, framestr, counts, agents

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
