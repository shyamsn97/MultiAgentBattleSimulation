import torch
import torch.nn.functional as F
import numpy as np

def create_linear_torch(input_dims,output_dims,relu=True,batch_norm=False):
    layers = []
    lin = torch.nn.Linear(input_dims,output_dims)
    layers.append(lin)
    if batch_norm:
        layers.append(torch.nn.BatchNorm1d(output_dims))
    if relu:
        layers.append(torch.nn.ReLU())
    return torch.nn.Sequential(*layers)

class TorchEstimator(torch.nn.Module):
    def __init__(self,view_range,move_range,attack_range):
        super(TorchEstimator,self).__init__()
        view_range = (1 + view_range*2)**2
        move_range = (1 + move_range*2)**2
        attack_range = (1 + attack_range*2)**2
        self.linear = create_linear_torch(3*view_range,32)
        self.linear2 = create_linear_torch(32,16)
        self.linear3 = create_linear_torch(16,move_range + attack_range,relu=False)
        self.softmax = torch.nn.Softmax(dim=-1)

    def forward(self,x,actions):
        x = self.linear(x)
        x = self.linear2(x)
        x = self.linear3(x)
        # print(x.size())
        x = self.softmax(x)
        x = x*actions
        x = x / x.sum(0)
        return x