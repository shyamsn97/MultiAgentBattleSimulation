import numpy as np
import random
from .Models import TorchEstimator
from .Memory import Memory
import torch

class Agent():
    def __init__(self,agentId,max_life,team,identity=0,viewrange=2,attackrange=1,moverange=2,estimator=None):
        self.agentId = agentId
        self.position = None
        self.estimator = estimator
        if estimator == None:
            self.estimator = TorchEstimator(viewrange,moverange,attackrange)
        self.max_life = max_life
        self.life = max_life
        self.reward = 0
        self.alive = True
        self.team = team
        self.identity = identity
        self.viewrange = viewrange
        self.attackrange = attackrange
        self.moverange = moverange
        self.damage = 100
        self.memory = Memory()
        self.living_reward = 1
        self.create_model()

    #getters
    def getMem(self):
        return self.memory

    def getLivingReward(self):
        return self.living_reward

    def getId(self):
        return self.agentId

    def getPosition(self):
        return self.position

    def getEstimator(self):
        return self.estimator

    def getLife(self):
        return self.life

    def getReward(self):
        return self.reward

    def isAlive(self):
        return self.alive

    def getTeam(self):
        return self.team

    def getIdentity(self):
        return self.identity

    def getViewRange(self):
        return self.viewrange

    def getAttackRange(self):
        return self.attackrange

    def getMoveRange(self):
        return self.moverange

    def getDamage(self):
        return self.damage

    #setters
    def setEstimator(self,estimator):
        self.estimator = estimator

    def setPosition(self,coord):
        self.position = coord

    def setViewRange(self,r):
        self.viewrange = r

    def setAttackRange(self,r):
        self.attackrange = r

    #processers
    def memorize(self,state,action,valid_actions,reward,action_probs=None):
        self.memory.add(state,action,valid_actions,reward,action_probs)

    def decay_reward(self):
        pass

    def flush(self):
        self.position = None
        self.life = self.max_life
        self.reward = 0
        self.alive = True

    def deliverDamage(self,damage,target_agent):
        self.reward += damage
        out_reward, alive = target_agent.processDamage(damage)
        return out_reward, alive

    def processDamage(self,damage):
        self.life -= damage
        self.reward -= damage
        out_reward = damage
        if self.life <= 0:
            self.alive = False
            self.reward -= 100
            out_reward = 100
        return out_reward, self.alive

    def updateLocation(self,coord):
        self.position = coord

    def create_model(self):
        self.policy = self.random_policy

    def generateActionSpace(self):
        return np.zeros((1 + self.moverange*2)**2 + (1 + self.actionrange*2)**2)

    def getValidProbabilites(self,values,actions):
        v = values*actions
        return v / np.sum(v,-1)

    def act(self,state,valid_actions):
        return self.train_policy(state,valid_actions)
    
    def train_policy(self,state,valid_actions):
        with torch.no_grad():
            tens_state = torch.tensor(state).float()
        probs = self.estimator(tens_state)
        #print("PROBS",probs)
        action_probs = probs.clone().detach().numpy().flatten()
        action_probs = self.getValidProbabilites(action_probs,valid_actions)
        return np.random.choice(action_probs.shape[0],p=action_probs), action_probs

    def save(self,state,action,reward,probs):
        self.mem.add(state,action,reward,probs)

    def move(self,action):
        self.position = action

    def random_policy(self,probs):
        return random.choice(len(probs),p=probs)

    def serialize(self):
        return {"agentId":self.agentId,"alive":self.alive,"team":self.team,"life":self.life,
                "position":self.position,"identity":self.identity,
                "viewrange":self.viewrange,"attackrange":self.attackrange,"reward":self.reward}

