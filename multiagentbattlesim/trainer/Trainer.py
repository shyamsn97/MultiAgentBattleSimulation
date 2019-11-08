import numpy as np

from tqdm import tqdm


class Trainer:
    def __init__(self, name):
        self.name = name

    def train_rule(self, agent, **kwargs):
        pass

    def train(self, epochs=50, **kwargs):
        self.epoch_bar = tqdm(np.arange(epochs))
