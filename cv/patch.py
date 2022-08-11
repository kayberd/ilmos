import os
import cv2
import utils

from PIL import Image

finalSize = (150, 150)
recordsDir = 'records/'
patchPath = f'patches_{finalSize[0]}/'

videos = os.listdir(recordsDir)

if not os.path.exists(patchPath):
    os.mkdir(patchPath)

for video in videos:
    videoPath = recordsDir + video
    fileName = video.split('.')[0]
    outDir = patchPath + fileName + '/'

    if os.path.exists(outDir):
        continue

    os.mkdir(outDir)   # if outDir not exists
    for i in range(1, 17): os.mkdir(outDir + f'patch{i}')

    cap = cv2.VideoCapture(videoPath)

    if (cap.isOpened() == False):
        raise Exception(f'Error while trying to read {video}')

    try:
        frameIndex = 0
        while(cap.isOpened()):
            ret, frame = cap.read() # numpy.ndarray
            if not ret: break

            patches = utils.getPatches(frame)
            for patch in patches:
                # cv2.imshow(f'patch{patchIndex}', patch[1])
                # cv2.waitKey(0)
                # continue
                patchDir = outDir + f"patch{patch[0]}/"
                Image.fromarray(patch[1]).resize(finalSize).save(patchDir + f'{fileName}_{frameIndex}_{patch[0]}.png')

            frameIndex += 1
            # break

    except KeyboardInterrupt:
        break