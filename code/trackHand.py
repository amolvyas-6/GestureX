import HandTrackingModule as htm
import cv2
import numpy as np

# Create a VideoCapture object and read from input file
cap = cv2.VideoCapture('tracking_video3.mp4')
tracker = htm.HandTracker(maxHands=1)

if (cap.isOpened()== False):
    print("Error opening video file")


output_video = 'output_video.mp4'
# Get video properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4

# Initialize the VideoWriter
video_writer = cv2.VideoWriter(output_video, fourcc, fps, (frame_width, frame_height))

history = []
flag = False
hand2 = 'Left'
lndmarks2 = []
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('p'):
            flag = True
        if key == ord('q'):
            break
        #frame = cv2.resize(frame, (640, 480))
        frame = tracker.findHands(frame)
        lndmarks, hand = tracker.getPoints(frame, handNo=0)
        if tracker.numOfHands(frame) == 2:
            lndmarks2, hand2 = tracker.getPoints(frame, handNo=1)
        if hand == 'Left':        
            if len(lndmarks) > 0 and flag:
                history.append(lndmarks[8])
        elif hand2 == 'Left':
            if len(lndmarks2) > 0 and flag:
                history.append(lndmarks2[8])
    else:
        break
    # for i in range(len(history) - 1):
    #     start_point = history[i]
    #     end_point = history[i + 1]
    #     color = (0, 255, 0)  # Green color for the line
    #     thickness = 2  # Thickness of the line
    #     cv2.line(frame, start_point, end_point, color, thickness)
    if len(history) > 1:
        pts = np.array(history, dtype=np.int32)
         # Simplify the polygon using contour approximationp
        epsilon = 0.05 * cv2.arcLength(pts, closed=False)  # Adjust the value of 0.02 for more/less simplification
        approx_pts = cv2.approxPolyDP(pts, epsilon, closed=False)
        cv2.polylines(frame, [approx_pts], isClosed=False, color=(0, 255, 0), thickness=2)
    video_writer.write(frame)
    cv2.imshow('Frame', frame)

cap.release()
cv2.imshow('Frame', frame)
