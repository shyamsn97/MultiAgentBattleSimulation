import numpy as np
import tqdm

from board import Board
from agent import Agent
from tools import *

class Game():
    def __init__(self,size,num_agents=1,max_life=100,configs=None):
        self.size = size
        self.board = Board(size)
        self.agent_configs = {"num_agents":num_agents,"max_life":max_life}
        if configs == None:
            self.initialize()

    def initialize(self):
        c = 0
        self.agents = []
        num_agents = self.agent_configs["num_agents"]
        max_life = self.agent_configs["max_life"]
        while c < num_agents:
            coord = (np.random.choice(self.size),np.random.choice(self.size))
            if self.board.getCell(coord) == 0:
                c += 1
                self.board.place(1,coord)
                self.agents.append(Agent(coord,max_life))

    def play(self):
        newpositions = set()
        for a in self.agents:
            prev = a.position
            actions = self.board.getMoves(prev)
            action = a.policy(actions)
            if action not in newpositions:
                a.makeAction(action)
                newpositions.add(action)
                self.board.place(0,prev)
                self.board.place(1,action)
        return self.board.encode(), self.board.__str__()

    def playEpisodes(self,num_episodes,pyg=False):
        frames = []
        framestr = []
        bar = tqdm.tqdm(np.arange(num_episodes))
        for i in bar:
            board, boardstr = self.play()
            frames.append(board)
            framestr.append(boardstr)
            bar.set_description("Episode: {}".format(i))
        # if pyg:
        #     playGrid(frames)
        # else:
        #     animate(framestr)
        return frames

    def printBoard(self):
        print(self.board)

if __name__ == "__main__":
    game = Game(20,num_agents=1)
    # game.printBoard()
    frames = game.playEpisodes(100)
