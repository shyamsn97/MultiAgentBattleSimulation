import numpy as np
import random

class Agent():
    def __init__(self,agentId,coord,max_life,team,identity=0,viewrange=1,attackrange=1):
        self.agentId = agentId
        self.position = coord
        self.estimator = None
        self.life = max_life
        self.reward = 0
        self.alive = True
        self.team = team
        self.identity = identity
        self.viewrange = viewrange
        self.attackrange = attackrange
        self.damage = 100
        self.create_model()
    #getters
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

    def getDamage(self):
        return self.damage

    #setters
    def setPosition(self,coord):
        self.position = coord

    def setViewRange(self,r):
        self.viewrange = r

    def setAttackRange(self,r):
        self.attackrange = r

    #processers
    def deliverDamage(self,damage,target_agent):
        self.reward += damage
        alive = target_agent.processDamage(damage)
        if alive == False:
            self.reward += 50
        return alive

    def processDamage(self,damage):
        self.life -= damage
        self.reward -= damage
        if self.life <= 0:
            self.alive = False
            self.reward -= 100
        return self.alive

    def update(self,coord,reward):
        self.position = coord
        self.reward += reward

    def create_model(self):
        self.policy = self.random_policy

    def train_policy(self,actions):
        return self.random_policy(actions)

    def move(self,action):
        self.position = action

    def random_policy(self,actions):
        return random.choice(actions)

    def serialize(self):
        return {"agentId":self.agentId,"alive":self.alive,"team":self.team,"life":self.life,
                "position":self.position,"identity":self.identity,
                "viewrange":self.viewrange,"attackrange":self.attackrange,"reward":self.reward}

