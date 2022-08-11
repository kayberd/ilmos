import torch
import torch.nn as nn
import torch.optim as optim
import torch.backends.cudnn as cudnn

import numpy as np
import matplotlib.pyplot as plt
import time
import os
import wandb
import random
import string

from torch.optim import lr_scheduler
from torchvision import datasets
from model import Classifier
from transforms import dataTransforms
from utils import parse

def train(model, criterion, optimizer, scheduler, num_epochs=50):
    since = time.time()
    best_acc = 0.0

    for epoch in range(num_epochs):
        # print(f'Epoch {epoch+1}/{num_epochs}')
        # print('-' * 10)

        logs = {
            'losses': {
                'train': None,
                'val': None
            },
            'accs': {
                'train': None,
                'val': None
            }
        }

        # Each epoch has a training and validation phase
        for phase in ['train', 'val']:
            if phase == 'train':
                model.train()  # Set model to training mode
            else:
                model.eval()   # Set model to evaluate mode

            running_loss = 0.0
            running_corrects = 0

            # Iterate over data.
            for inputs, labels in dataloaders[phase]:
                inputs = inputs.to(device)
                labels = labels.to(device)

                # zero the parameter gradients
                optimizer.zero_grad()

                # forward
                # track history if only in train
                with torch.set_grad_enabled(phase == 'train'):  # torch.no_grad()
                    outputs = model(inputs)
                    _, preds = torch.max(outputs, 1)
                    loss = criterion(outputs, labels)

                    # backward + optimize only if in training phase
                    if phase == 'train':
                        loss.backward()
                        optimizer.step()

                # statistics
                running_loss += loss.item() * inputs.size(0)
                running_corrects += torch.sum(preds == labels.data)
            if phase == 'train':
                scheduler.step()

            epoch_loss = running_loss / datasetSizes[phase]
            epoch_acc = running_corrects.double() / datasetSizes[phase]

            logs['losses'][phase] = epoch_loss
            logs['accs'][phase] = epoch_acc

            # print(f'{phase} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f}')

            # deep copy the model
            if phase == 'val' and epoch_acc > best_acc:
                best_acc = epoch_acc
                model.save(epoch+1, config, trainingID)

        # print()
        wandb.log({
            "training_loss": logs['losses']['train'],
            "val_loss": logs['losses']['val'],
            "val_acc": logs['accs']['val']
        })

    time_elapsed = time.time() - since
    print(f'training ID: {trainingID}')
    print(f'Training complete in {time_elapsed // 60:.0f}m {time_elapsed % 60:.0f}s')
    print(f'Best val Acc: {best_acc:4f}')

    return model

if __name__ == '__main__':
    # args = parse()  # {'batch_size': ..., 'learning_rate': ...}
    # batchSize = args['batch_size']
    # learningRate = args['learning_rate']
    # H1 = args['H1']
    # H2 = args['H2']
    # stepSize = args['step_size']
    # gamma = args['gamma']

    batchSizes = [16]
    learningRates = [0.0001]#, 0.0005]
    gammas = [0.5]#[0.9, 0.5, 0.3]
    stepSize = 10
    weight_decay = 0
    momentum = 0.9

    cudnn.benchmark = True  # fixed size inputs

    imageDatasets = {x: datasets.ImageFolder(os.path.join('dset', x),
                                            dataTransforms[x])
                    for x in ['train', 'val']}

    datasetSizes = {x: len(imageDatasets[x]) for x in ['train', 'val']}
    #classNames = imageDatasets['train'].classes

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    criterion = nn.CrossEntropyLoss()

    for batchSize in batchSizes:
        dataloaders = {x: torch.utils.data.DataLoader(imageDatasets[x], batch_size=batchSize,
                                                shuffle=True, num_workers=4)
                for x in ['train', 'val']}

        for learningRate in learningRates:
            for gamma in gammas:
                classifier = Classifier().to(device)
                trainingID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

                config = {
                    'trainingID': trainingID,
                    "learning_rate": learningRate,
                    "batch_size": batchSize,
                    "weight_decay": weight_decay,
                    "momentum": momentum,
                    "lr_scheduler": {
                        "step_size": stepSize,
                        "gamma": gamma
                    }
                }
                wandb.init(
                    project = "ilmos",
                    name = f"CJ_ResNet18_bs{batchSize}_lr{learningRate}_gamma{gamma}_wd{weight_decay}",
                    config = config
                )
                optimizer_ft = optim.SGD(classifier.parameters(), lr=learningRate, momentum=momentum, weight_decay=weight_decay)

                # Decay LR by a factor of gamma every stepSize epochs
                lr_scheduler = lr_scheduler.StepLR(optimizer_ft, step_size=stepSize, gamma=gamma)

                classifier = train(classifier, criterion, optimizer_ft, lr_scheduler,
                    num_epochs=50)

                wandb.finish()