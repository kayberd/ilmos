import cv2
import torch
import requests
import credentials
import json
from credentials import updateSeatURL

_COLOUR = (0, 0, 255)
_THICKNESS = 5
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
    {"status": "", "signal": [0]*_NOISE_MARGIN},
    {"status": "", "signal": [0]*_NOISE_MARGIN},
    {"status": "", "signal": [0]*_NOISE_MARGIN},
    {"status": "", "signal": [0]*_NOISE_MARGIN},

    {"status": "", "signal": [0]*_NOISE_MARGIN},
    {"status": "", "signal": [0]*_NOISE_MARGIN},
    {"status": "", "signal": [0]*_NOISE_MARGIN},
    {"status": "", "signal": [0]*_NOISE_MARGIN},

    {"status": "", "signal": [0]*_NOISE_MARGIN},
    {"status": "", "signal": [0]*_NOISE_MARGIN},
    {"status": "", "signal": [0]*_NOISE_MARGIN},
    {"status": "", "signal": [0]*_NOISE_MARGIN},

    {"status": "", "signal": [0]*_NOISE_MARGIN},
    {"status": "", "signal": [0]*_NOISE_MARGIN},
    {"status": "", "signal": [0]*_NOISE_MARGIN},
    {"status": "", "signal": [0]*_NOISE_MARGIN}
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
        #print(f"{'#'*10} Set seat {id} to {newStatus} {'#'*10}")
        DESK_STATUS[id-1]['status'] = newStatus

        # print("*"*10 + "BEFORE REQUEST" + "*"*10)

        requests.put(f"{updateSeatURL}/{id}", data=json.dumps({"status": newStatus}), headers={"Content-Type": "application/json"})

        # print("#"*11 + "AFTER REQUEST" + "#"*10)

def getPatches(frameQueue, patchQueue):
    while True:
        result = list()
        frame = frameQueue.get()
        #print("frameQueue -= 1")

        for patch in PATCHES:
            result.append( (patch["id"], frame[patch["min_y"]: patch["max_y"], patch["min_x"]: patch["max_x"]]) )

        patchQueue.put((frame, result))
        #print("patchQueue += 1")

def capture(frameQueue):
    while True:
        cap = cv2.VideoCapture(credentials.URL)
        try:
            while(cap.isOpened()):
                    ret, frame = cap.read()     # numpy.ndarray
                    if not ret: break
                    frameQueue.put(frame)
                    #print("frameQueue += 1")
        except:
            #print("Capture process crashed")