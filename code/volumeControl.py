import HandTrackingModule as htm
import getGesture as gg
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

volumePrev = 0
smoothening = 5

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    img = tracker.findHands(img)
    landmarkPoints = []
    landmarkPoints2 = []
    
    num_hands = tracker.numOfHands(img)

    left = []
    right = []

    if num_hands > 0:
        if num_hands == 1:
            landmarkPoints, hand1_label = tracker.getPoints(img, handNo=0)
            if hand1_label == 'Left':
                left = landmarkPoints
                right = []
            else:
                left = []
                right = landmarkPoints

        elif num_hands == 2:
            landmarkPoints, hand1_label = tracker.getPoints(img, handNo=1)
            landmarkPoints2, hand2_label = tracker.getPoints(img, handNo=0)
            
            if hand1_label == 'Left' and hand2_label == 'Right':
                left = landmarkPoints
                right = landmarkPoints2
            else:
                right = landmarkPoints
                left = landmarkPoints2

        if len(left) > 0:
            img = tracker.drawBoundingBox(img, points=tracker.getBoundingBox(img, left), color=(0,0,255))
            if gg.get_prediction(left) == 'Thumbs Up':
                break

        if len(right) > 0:
            img = tracker.drawBoundingBox(img, points=tracker.getBoundingBox(img, right))
            length = tracker.getLength(right[4], right[8])
            volume = int((((length - minLen) * NewRange) / OldRange) + minVol)

            volume = volumePrev + (volume - volumePrev) / smoothening
            volume = max(0, min(100, volume))
            volume_scaled = volume / 100
            volume_pycaw.SetMasterVolumeLevelScalar(volume_scaled, None)
            volumePrev = volume

    cv2.imshow('VolumeControl', img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


