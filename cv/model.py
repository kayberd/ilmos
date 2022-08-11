import os
import string
import json
import torch
import torch.nn as nn
import numpy as np

from torchvision import models

class Classifier(nn.Module):
    def __init__(self, H1=32, H2=8):
        super(Classifier, self).__init__()

        self.H1 = H1
        self.H2 = H2

        self.model = models.resnet18(pretrained = True)
        self.model.fc = nn.Sequential(
            nn.Linear(self.model.fc.in_features, H1),
            nn.ReLU(),
            nn.Linear(H1, H2),
            nn.ReLU(),
            nn.Linear(H2, 2)
        )

    def forward(self, input):
        if len(input.shape) == 3:
            input = torch.unsqueeze(input, 0)
        return self.model(input)

    def save(self, epoch, config, trainingID):
        path = f"checkpoints/{trainingID}"

        if not os.path.exists('checkpoints'):
            os.mkdir('checkpoints')

        if not os.path.exists(path):
            os.mkdir(path)

        torch.save(self.model.state_dict(), f"{path}/epoch_{epoch}.pt")

        fd = open(f"{path}/config.json", "w")
        json.dump(config, fd)
        fd.close()

    def load(self, path):
        self.model.load_state_dict(torch.load(path, map_location=torch.device('cpu')))