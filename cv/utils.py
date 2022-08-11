import cv2
import numpy as np
import torch
import requests
import argparse
import json

from model import Classifier
from credentials import updateSeatURL
from PIL import Image

_COLOUR = (255, 255, 0)
_THICKNESS = 2
_NOISE_MARGIN = 5

"""
    --> x [0,1920)
    |
    |
    v   y [0, 1080)

    shape[0] -> y
    shape[1] -> x
"""

# Patches belonging to individual desks, will be manually input.
PATCHES = [
    # bottom left desk
    {"id": 1, "min_x": 0, "max_x": 300, "min_y": 600, "max_y": 1080},
    {"id": 2, "min_x": 300, "max_x": 680, "min_y": 600, "max_y": 1080},
    {"id": 3, "min_x": 150, "max_x": 450, "min_y": 300, "max_y": 600},
    {"id": 4, "min_x": 450, "max_x": 750, "min_y": 300, "max_y": 600},
    
    # # bottom right desk
    {"id": 5, "min_x": 1250, "max_x": 1650, "min_y": 600, "max_y": 1080},
    {"id": 6, "min_x": 1650, "max_x": 1920, "min_y": 600, "max_y": 1080},
    {"id": 7, "min_x": 1150, "max_x": 1450, "min_y": 300, "max_y": 600},
    {"id": 8, "min_x": 1450, "max_x": 1720, "min_y": 300, "max_y": 600},

    # top left desk
    {"id": 9, "min_x": 380, "max_x": 580, "min_y": 160, "max_y": 300},
    {"id": 10, "min_x": 580, "max_x": 760, "min_y": 160, "max_y": 300},
    {"id": 11, "min_x": 500, "max_x": 650, "min_y": 75, "max_y": 160},
    {"id": 12, "min_x": 650, "max_x": 800, "min_y": 75, "max_y": 160},

    # top right desk
    {"id": 13, "min_x": 1070, "max_x": 1260, "min_y": 150, "max_y": 300},
    {"id": 14, "min_x": 1260, "max_x": 1450, "min_y": 150, "max_y": 300},
    {"id": 15, "min_x": 1030, "max_x": 1200, "min_y": 50, "max_y": 150},
    {"id": 16, "min_x": 1200, "max_x": 1370, "min_y": 50, "max_y": 150},
]

DESK_STATUS = [
    {"status": "VACANT", "signal": [0]*_NOISE_MARGIN},
    {"status": "VACANT", "signal": [0]*_NOISE_MARGIN},
    {"status": "VACANT", "signal": [0]*_NOISE_MARGIN},
    {"status": "VACANT", "signal": [0]*_NOISE_MARGIN},

    {"status": "VACANT", "signal": [0]*_NOISE_MARGIN},
    {"status": "VACANT", "signal": [0]*_NOISE_MARGIN},
    {"status": "VACANT", "signal": [0]*_NOISE_MARGIN},
    {"status": "VACANT", "signal": [0]*_NOISE_MARGIN},

    {"status": "VACANT", "signal": [0]*_NOISE_MARGIN},
    {"status": "VACANT", "signal": [0]*_NOISE_MARGIN},
    {"status": "VACANT", "signal": [0]*_NOISE_MARGIN},
    {"status": "VACANT", "signal": [0]*_NOISE_MARGIN},

    {"status": "VACANT", "signal": [0]*_NOISE_MARGIN},
    {"status": "VACANT", "signal": [0]*_NOISE_MARGIN},
    {"status": "VACANT", "signal": [0]*_NOISE_MARGIN},
    {"status": "VACANT", "signal": [0]*_NOISE_MARGIN}
]

def updateStatus(id, signal):
    oldSignal = DESK_STATUS[id-1]['signal']

    # no need to update signal accumulator
    if signal == "VACANT" and sum(oldSignal) == -_NOISE_MARGIN:
        return
    elif signal == "TAKEN" and sum(oldSignal) == _NOISE_MARGIN:
        return

    DESK_STATUS[id-1]['signal'] = oldSignal[1:]
    DESK_STATUS[id-1]['signal'].append(-1 if signal == "VACANT" else 1)

    newStatus = "TAKEN" if sum(DESK_STATUS[id-1]['signal']) > 0 else "VACANT"

    if DESK_STATUS[id-1]['status'] != newStatus:
        # print(f"Set seat {id} to {newStatus}")
        DESK_STATUS[id-1]['status'] = newStatus
        requests.put(f"{updateSeatURL}/{id}", data=json.dumps({"status": newStatus}), headers={"Content-Type": "application/json"})

def getPatches(frame: np.ndarray):
    result = list()

    for patch in PATCHES:
        result.append( (patch["id"], frame[patch["min_y"]: patch["max_y"], patch["min_x"]: patch["max_x"]]) )

    return result

def visualizePredictions(model: Classifier, frame: np.ndarray, transforms, device):
    patches = getPatches(frame)

    for id, patch in patches:
        _patch = Image.fromarray(patch).resize((150, 150))
        tensor = transforms(_patch).to(device)
        _, pred = torch.max(model(tensor), 1)

        signal = "TAKEN" if pred[0] == 0 else "VACANT"

        minCoords = PATCHES[id-1]["min_x"], PATCHES[id-1]["min_y"]
        maxCoords = PATCHES[id-1]["max_x"], PATCHES[id-1]["max_y"]

        if signal == "TAKEN" and sum(DESK_STATUS[id-1]['signal']) == _NOISE_MARGIN:   # show taken seats only
            cv2.putText(frame, signal, (minCoords[0], minCoords[1]-5), cv2.FONT_HERSHEY_SIMPLEX, 1, _COLOUR, _THICKNESS)
            cv2.rectangle(frame, minCoords, maxCoords, _COLOUR, _THICKNESS)

        updateStatus(id, signal)

    return frame

def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('-bs', '--batch-size', default=4, type=int)
    parser.add_argument('-lr', '--learning-rate', default=1e-3, type=float)
    parser.add_argument('--H1', default=32, type=int)
    parser.add_argument('--H2', default=8, type=int)
    parser.add_argument('-ss', '--step-size', default=10, type=int)
    parser.add_argument('-g', '--gamma', default=0.5, type=int)

    return vars(parser.parse_args())
