import utils
import cv2

video = 'records/2022-04-28-11.mp4'
cap = cv2.VideoCapture(video)

try:
    while(cap.isOpened()):
        ret, frame = cap.read() # numpy.ndarray
        if not ret: break

        frame = utils.visualizePatches(frame)
        cv2.imshow('patches', frame)
        cv2.waitKey(0)
except KeyboardInterrupt:
    cap.release()