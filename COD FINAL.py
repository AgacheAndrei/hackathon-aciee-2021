from collections import deque
from imutils.video import VideoStream
import numpy as np
import cv2
import argparse
import time
import imutils
import os
import RPi.GPIO as GPIO
# GPIO.setmode(GPIO.BOARD)
# 
# GPIO.setwarnings(False)
# 
# GPIO.setup(11,GPIO.OUT)
# panServo = GPIO.PWM(11,50)
# GPIO.setup(12,GPIO.OUT)
# tiltServo = GPIO.PWM(12,50)
# 
# panServo.start(0)
# tiltServo.start(0)

panServo = 17
tiltServo = 27

#position servos 
def positionServo (servo, angle):
    os.system("python angleServoCtrl.py " + str(servo) + " " + str(angle))
    print("[INFO] Positioning servo at GPIO {0} to {1} degrees\n".format(servo, angle))

# position servos to present object at center of the frame
def mapServoPosition (x, y):
    global panAngle
    global tiltAngle
    if (x < 220):
        panAngle += 5
        if panAngle > 140:
            panAngle = 140
        positionServo (panServo, panAngle)
 
    if (x > 280):
        panAngle -= 5
        if panAngle < 40:
            panAngle = 40
        positionServo (panServo, panAngle)

    if (y < 160):
        tiltAngle += -5
        if tiltAngle > 140:
            tiltAngle = 140
        positionServo (tiltServo, tiltAngle)
 
    if (y > 210):
        tiltAngle -= -5
        if tiltAngle < 40:
            tiltAngle = 40
        positionServo (tiltServo, tiltAngle)
        
# Initialize angle servos at 90-90 position
global panAngle
panAngle = 90
global tiltAngle
tiltAngle =90

# positioning Pan/Tilt servos at initial position
positionServo (panServo, panAngle)
positionServo (tiltServo, tiltAngle)

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", help="Path to the (optional) video file")
ap.add_argument("-b", "--buffer", default=64, type=int, help="max buffer size")
args = vars(ap.parse_args())

greenLower =(0,190,75)
greenUpper = (169,255,255)
pts = deque(maxlen=args["buffer"])



if not args.get("video", False):
    vs = VideoStream(src=0).start()
else:
    vs = cv2.VideoCapture(0)
    vs.set(cv2.CAP_PROP_FPS,40)
    fps = int(vs.get(5))
    print (fps)

#time.sleep(2.0)


while True:
    frame = vs.read()
#merge si fara asta     f
#    frame = cv2.flip(frame,-1)
    frame = frame[1] if args.get("video", False) else frame
    if frame is None:
        break
    frame = imutils.resize(frame, width=500)
    frame = imutils.rotate(frame, angle=180)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    bgr = cv2.cvtColor(blurred, cv2.COLOR_HSV2BGR)


    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M['m10']/M['m00']), int(M['m01']/M['m00']))

        if radius > 10:
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 0), -1)
            mapServoPosition(int(x), int(y))
            print("PRINT X= " +str(int(x)))
            print("PRINT Y= " +str(int(y)))
            text = "PRINT X= " +str(int(x))+"  "+"PRINT Y= " +str(int(y))
            coordinates = (40,50)
            coordinates2 = (40,80)
            coordinates3 = (40,100)
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 0.5
            color = (255,0,255)
            thickness = 1
            if int(x) <250:
                frame = cv2.putText(frame, text, coordinates, font, fontScale, color, thickness, cv2.LINE_AA)
                frame = cv2.putText(frame, "stanga", coordinates2, font, fontScale, color, thickness, cv2.LINE_AA) 
            elif int(x) >250:
                frame = cv2.putText(frame, text, coordinates, font, fontScale, color, thickness, cv2.LINE_AA)
                frame = cv2.putText(frame, "dreapta", coordinates2, font, fontScale, color, thickness, cv2.LINE_AA) 
            if int(y)<250:
                frame = cv2.putText(frame, text, coordinates, font, fontScale, color, thickness, cv2.LINE_AA)
                frame = cv2.putText(frame, "sus", coordinates3, font, fontScale, color, thickness, cv2.LINE_AA) 
            elif int(y)>250:
                frame = cv2.putText(frame, text, coordinates, font, fontScale, color, thickness, cv2.LINE_AA) 
                frame = cv2.putText(frame, "jos", coordinates3, font, fontScale, color, thickness, cv2.LINE_AA)        
    pts.append(center)
#coditele
    for i in range(1, len(pts)):
        if pts[i-1] is None or pts[i] is None:
            continue

        thickness = int(np.sqrt(args["buffer"] / float(i+1)) * 2)
        cv2.line(frame, pts[i-1], pts[i], (20, 247, 255), thickness)

    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break

if not args.get("video", False):
    vs.stop()
else:
    vs.release()

positionServo (panServo, 90)
positionServo (tiltServo, 90)
GPIO.cleanup()
cv2.destroyAllWindows()
