import numpy as np
import tqdm
import random

from Env import Env
from agent import Agent
from tools import *

class Game():
    def __init__(self,size,num_agents=1,max_life=100,viewrange=2,num_teams=2,
                num_episodes=20,episode_length=200,configs=None):
        self.size = size
        self.env = Env(size,num_teams)
        self.agent_configs = {"num_agents":num_agents,"max_life":max_life,"viewrange":viewrange}
        self.agent_dict = {}
        self.num_teams = num_teams
        self.num_episodes = num_episodes
        self.episode_length = episode_length
        self.living_reward = 1
        self.death_reward = -100
        self.kill_reward = 50
        if configs == None:
            self.createAgents()

    #getters
    def getNumTeams(self):
        return self.num_teams

    def getAgents(self):
        return self.agent_dict
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
                self.agent_dict[agentId] = agent

    def initialize(self):
        self.env.initialize(self.agent_dict)

    def step(self):
        l = list(self.agent_dict.keys())
        random.shuffle(l) #shuffle agent order
        for agentId in l:
            agent = self.agent_dict[agentId]
            if agent.isAlive():
                agent.update_history()
                states, actions, coord_list = self.env.getStatesActions(agent)
                action, action_probs = agent.train_policy(states,actions)
                reward = self.env.step(agent,action,coord_list)
        agent_count, team_count = self.env.countAgents(self.num_teams)
        return self.env.encode(), self.env.__str__(),agent_count, team_count, self.serializeAgents()

    def playEpisodes(self,pyg=False):
        frames = []
        framestr = []
        agent_counts = [self.env.countAgents(self.num_teams)]
        agents = [self.serializeAgents()]
        team_counts = [[self.agent_configs["num_agents"]]*self.num_teams]
        num_episode_bar = tqdm.tqdm(np.arange(self.num_episodes))
        for i in num_episode_bar:
            self.initialize()
            episode_bar = tqdm.tqdm(np.arange(self.episode_length))
            for j in episode_bar:
                encoded, envstr, agent_count, team_count, serialized_agents = self.step()
                frames.append(encoded)
                framestr.append(envstr)
                agents.append(serialized_agents)
                agent_counts.append(agent_count)
                team_counts.append(team_count)
                episode_bar.set_description("Episode {} - Step {}: with agent count {}".format(i,j,agent_count))
        # if pyg:
        #     playGrid(frames)
        # else:
        #     animate(framestr)
        return frames, framestr, agent_counts, team_counts, agents

    def serializeAgents(self):
        serialized = {}
        for agentId in self.agent_dict.keys():
            agent = self.agent_dict[agentId]
            serialized[agentId] = agent.serialize()
        return serialized

    def printEnv(self):
        print(self.env)

if __name__ == "__main__":
    game = Game(20,num_agents=1)
    frames = game.playEpisodes(100)
