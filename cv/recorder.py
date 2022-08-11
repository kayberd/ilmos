import os
import sys
import cv2
import credentials
import datetime

from PIL import Image

dropRate = int(sys.argv[1]) if len(sys.argv) > 1 else 600    # grab a frame every 10 minutes
cap = cv2.VideoCapture(credentials.URL)

print(f'dropRate: {dropRate}')

assert cap.isOpened(), 'Error reaching the camera'

outName = datetime.datetime.now().strftime("%Y-%m-%d-%H")

if not os.path.exists('records/'):
    os.mkdir('records/')

# define codec and create VideoWriter object 
out = cv2.VideoWriter(f"records/{outName}.mp4",
                      cv2.VideoWriter_fourcc(*'mp4v'), 1,
                      (int(cap.get(3)), int(cap.get(4))))
frameCount = 0
try:
    while(cap.isOpened()):
        for _ in range(dropRate): cap.grab()

        _, frame = cap.retrieve()   # numpy.ndarray
        out.write(frame)
        frameCount+=1
except KeyboardInterrupt:
    print(f'{frameCount} frames written to {outName}.mp4')
cap.release()
