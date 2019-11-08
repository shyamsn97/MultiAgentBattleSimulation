import torch


def create_linear_torch(input_dims, output_dims, relu=True, batch_norm=False):
    layers = []
    lin = torch.nn.Linear(input_dims, output_dims)
    layers.append(lin)
    if batch_norm:
        layers.append(torch.nn.BatchNorm1d(output_dims))
    if relu:
        layers.append(torch.nn.ReLU())
    return torch.nn.Sequential(*layers)


def getTorchProbs(probs, actions):
    with torch.no_grad():
        actions = torch.tensor(actions + 1e-3).float()
    v = probs * actions
    v = v / (v.sum(-1) + torch.tensor(1e-3))
    # print("VALID PROBS", v)
    return v + torch.tensor(1e-3)
