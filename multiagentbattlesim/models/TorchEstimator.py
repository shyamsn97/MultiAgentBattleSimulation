import torch
from multiagentbattlesim.utils import torch_utils


class TorchEstimator(torch.nn.Module):
    def __init__(self, view_range, move_range, attack_range):
        super(TorchEstimator, self).__init__()
        view_range = (1 + view_range * 2) ** 2
        move_range = (1 + move_range * 2) ** 2
        attack_range = (1 + attack_range * 2) ** 2
        self.linear = torch_utils.create_linear_torch(3 * view_range, 32)
        self.linear2 = torch_utils.create_linear_torch(32, 16)
        self.linear3 = torch_utils.create_linear_torch(
            16, move_range + attack_range, relu=False
        )
        self.softmax = torch.nn.Softmax(dim=-1)

    def forward(self, x):
        x = self.linear(x)
        x = self.linear2(x)
        x = self.linear3(x)
        x = self.softmax(x)
        return x
