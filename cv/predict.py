import cv2
import torch
import numpy as np
import credentials
import threading
import queue

from model import Classifier
from transforms import dataTransforms
from utils import visualizePredictions

def capture(q, signalQ):
    cap = cv2.VideoCapture('bugrik.mp4')    #(credentials.URL)
    while(cap.isOpened()):
        if signalQ.empty():
            ret, frame = cap.read() # numpy.ndarray
            if not ret: break
            q.put(frame)
        else:
            cap.release()
            break

if __name__ == '__main__':
    q = queue.Queue()
    signalQ = queue.Queue()
    captureThread = threading.Thread(target=capture, args=(q, signalQ))
    captureThread.start()

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    classifier = Classifier().to(device)
    classifier.load('old_checkpoint.pt')
    classifier.eval()

    transforms = dataTransforms['val']

    # out = cv2.VideoWriter("bugrik_predictions.mp4",
    #                   cv2.VideoWriter_fourcc(*'mp4v'), 1,
    #                   (1920, 1080))

    try:
        while True:
            print(f"Number of frames in the buffer: {q.qsize()}")
            frame = visualizePredictions(classifier, q.get(), transforms, device)
            # out.write(frame)
            cv2.imshow('predictions', frame)
            cv2.waitKey(1)

    except KeyboardInterrupt:
        signalQ.put("")
        captureThread.join()