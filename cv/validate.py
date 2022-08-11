import os
import torch
import torch.nn as nn
import torch.backends.cudnn as cudnn
import wandb

from torchvision import datasets
from model import Classifier
from utils import parse
from transforms import dataTransforms

def validate(model, criterion):
    # Single iteration
    for inputs, labels in dataloader:
        inputs = inputs.to(device)
        labels = labels.to(device)
        samples = dataloader.dataset.samples

        # forward
        with torch.no_grad():
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            loss = criterion(outputs, labels)

        # statistics
        running_loss = loss.item() * inputs.size(0)
        running_corrects = torch.sum(preds == labels.data)

    # wandb.log({
    #     "val_loss": running_loss / valSetSize,
    #     "val_acc": running_corrects.double() / valSetSize
    # })

    return samples, torch.stack((labels,preds), dim=1)

if __name__ == '__main__':
    cudnn.benchmark = True  # fixed size inputs

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    criterion = nn.CrossEntropyLoss()

    valSet = datasets.ImageFolder(os.path.join('dset', 'val'), dataTransforms['val'])
    valSetSize = len(valSet)
    dataloader = torch.utils.data.DataLoader(valSet, batch_size = valSetSize,
                                                shuffle=False, num_workers=4)

    classifier = Classifier().to(device)
    classifier.load('old_checkpoint.pt')
    classifier.eval()

    # wandb.init(
    #     project = "ilmos",
    #     name = f"val_UTHZ5B82_epoch_36"
    # )

    samples, stacked = validate(classifier, criterion)
    zipped = zip(samples, stacked)
    matrix = torch.zeros(2, 2, dtype=torch.int64)
    
    for sample, p in zipped:
        gt, pred = p.tolist()
        matrix[gt, pred] += 1

        if gt != pred:
            print(sample)

    print(matrix)
    # wandb.finish()