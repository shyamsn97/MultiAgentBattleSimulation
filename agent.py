import numpy as np
import random

class Agent():
    def __init__(self,coord,maxlife):
        self.position = coord
        self.estimator = None
        self.life = maxlife
        self.reward = 0
        self.alive = True
        self.create_model()
    #getters
    def getPosition(self):
        return getPosition
    #setters
    def setPosition(self,coord):
        self.position = coord

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

    def makeAction(self,action):
        self.position = action

    def random_policy(self,actions):
        return random.choice(actions)
