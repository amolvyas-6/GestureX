import HandTrackingModule as htm
import numpy as np
import cv2
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL

# Get the default audio device used for playback
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None
)
volume_pycaw = interface.QueryInterface(IAudioEndpointVolume)


cap = cv2.VideoCapture(0)
tracker = htm.HandTracker()

maxLen, minLen = 200, 25
maxVol, minVol = 100, 0
OldRange = (maxLen - minLen)  
NewRange = (maxVol - minVol)

while True:
    suc, img = cap.read()
    img = cv2.flip(img, 1)

    img = tracker.findHands(img)
    lndmrkPoints = []
    lndmrkPoints2 = []
    if tracker.numOfHands(img) == 1:
        lndmrkPoints = tracker.getPoints(img, handNo=0)
    else:
        lndmrkPoints = tracker.getPoints(img, handNo=1)
        lndmrkPoints2 = tracker.getPoints(img, handNo=0)
    
    if len(lndmrkPoints2) > 0:
        img = tracker.drawBoundingBox(img, points=tracker.getBoundingBox(img, lndmrkPoints2), color=(0,0,255))
    if len(lndmrkPoints) > 0:
        img = tracker.drawBoundingBox(img, points=tracker.getBoundingBox(img, lndmrkPoints), color=(255, 0, 0))
        length = tracker.getLength(lndmrkPoints[4], lndmrkPoints[8])
        volume = int((((length - minLen) * NewRange) / OldRange) + minVol)
        if volume > 100:
            volume = 100
        if volume < 0:
            volume = 0
        print(length, volume) 
        volume = volume / 100
        volume_pycaw.SetMasterVolumeLevelScalar(volume, None)
    
    cv2.imshow('VolumeControl', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


