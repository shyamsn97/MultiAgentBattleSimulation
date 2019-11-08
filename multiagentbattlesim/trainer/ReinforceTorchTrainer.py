import numpy as np

import torch
from multiagentbattlesim.trainer import Trainer
from multiagentbattlesim.utils import torch_utils
from tqdm import tqdm


class ReinforceTorchTrainer(Trainer):
    def __init__(self, estimator, epochs=20, learning_rate=0.00001):
        super(ReinforceTorchTrainer, self).__init__(name="reinforce")
        self.learning_rate = learning_rate
        self.model = {}
        self.model["estimator"] = estimator

        def loss(predictions, targets):
            return -1 * torch.sum(torch.mul(torch.log(predictions), targets))

        self.model["loss"] = loss
        self.model["optimizer"] = torch.optim.Adam(
            params=self.model["estimator"].parameters(), lr=self.learning_rate
        )

    def loss(predictions, targets):
        return -1 * torch.sum(torch.mul(torch.log(predictions), targets))

    def train(self, agent_dict):
        super(ReinforceTorchTrainer, self).train(epochs=10)
        # has experience memory, but only updates
        # obs_arr = []
        # reward_arr = []
        loss_fn = self.model["loss"]
        optimizer = self.model["optimizer"]
        temp_loss = 0
        agentLoss = 0
        for epoch in self.epoch_bar:
            self.epoch_bar.set_description("EPOCH {} LOSS: {}".format(epoch, temp_loss))
            temp_loss = 0
            agent_keys = list(agent_dict.keys())
            agent_bar = tqdm(np.arange(len(agent_keys)))
            for agentId in agent_bar:
                agent = agent_dict[agent_keys[agentId]]
                agent_bar.set_description("AGENT {} LOSS {}".format(agentId, agentLoss))
                agentLoss = 0
                for i in range(len(agent.memory)):
                    state, action, valid_actions, reward, action_probs = agent.memory[i]
                    state = torch.tensor(state).float()
                    probs = agent.estimator(state)
                    with torch.no_grad():
                        target = np.zeros_like(action_probs)
                        target[action] = float(reward)
                        target = torch.tensor(target).float()
                    probs = torch_utils.getTorchProbs(probs, valid_actions)
                    loss = loss_fn(probs, target)
                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()
                    agentLoss += loss.item()
                temp_loss += agentLoss / len(agent.memory)
