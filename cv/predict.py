import cv2
import torch
import utils

from PIL import Image
from multiprocessing import Process, Queue
from model import Classifier
from transforms import dataTransforms

if __name__ == '__main__':
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    classifier = Classifier().to(device)
    classifier.load('old_checkpoint.pt')
    classifier.eval()
    transforms = dataTransforms['val']

    frameQueue = Queue()
    patchQueue = Queue()

    captureProcess = Process(target=utils.capture, args=(frameQueue, ))
    captureProcess.start()

    patchProcess = Process(target=utils.getPatches, args=(frameQueue, patchQueue))
    patchProcess.start()

    # out = cv2.VideoWriter("_predictions.mp4",
    #                   cv2.VideoWriter_fourcc(*'mp4v'), 1,
    #                   (1920, 1080))

    windowName = 'Predictions made'
    cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)

    while True:
        frame, patches = patchQueue.get()

        for id, patch in patches:
            _patch = Image.fromarray(patch).resize((150, 150))
            tensor = transforms(_patch).to(device)
            _, pred = torch.max(classifier(tensor), 1)

            signal = "TAKEN" if pred[0] == 0 else "VACANT"
            utils.updateStatus(id, signal)

            minCoords = utils.PATCHES[id-1]["min_x"], utils.PATCHES[id-1]["min_y"]
            maxCoords = utils.PATCHES[id-1]["max_x"], utils.PATCHES[id-1]["max_y"]

            if utils.DESK_STATUS[id-1]['status'] == "TAKEN":   # show taken seats only
                cv2.putText(frame, "OCCUPIED", (minCoords[0], minCoords[1]-5), cv2.FONT_HERSHEY_SIMPLEX, 1, utils._COLOUR, utils._THICKNESS)
                cv2.rectangle(frame, minCoords, maxCoords, utils._COLOUR, utils._THICKNESS)

        cv2.imshow(windowName, frame)
        cv2.waitKey(1)
        # out.write(frame)