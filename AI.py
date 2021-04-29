import cv2
import os
import time
import numpy

# turn on camera
camera = cv2.VideoCapture(0)
# if camera is off, exit program
if not camera.isOpened():
    # change w proper error message
    print("Cannot open camera")
    exit()
# set up predator classifier file
predatorPath = os.path.join('Cascades', 'predatorFinder.xml')
predator_cascade = cv2.CascadeClassifier(predatorPath)
# set up human classifier file
humanPath = os.path.join('Cascades', 'humanFinder.xml')
human_cascade = cv2.CascadeClassifier(humanPath)


# run video to detect animal or human intruder
while (camera.isOpened()):
    # capture a frame from video
    isTrue, img = camera.read()
    if (isTrue):
        if (predator_cascade.empty() or human_cascade.empty()):
            print("empty")
        # convert image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # detect predator face in frame
        predators = predator_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=2)
        # detect human in frame
        humans = human_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=1)
        if len(predators) > 0:
            for (x,y,w,h) in predators:
                cv.rectangle(img, (x,y), (x+w,y+h), (255,0,0), thickness=2)
            # alert farmer of predator
            cv.imshow("Intruder Cat", img)
        if len(humans) > 0:
            for (x,y,w,h) in humans:
                cv.rectangle(img, (x,y), (x+w,y+h), (0,255,0), thickness=2)
             # alert farmer of human
            cv.imshow("Intruder", img)
    else:
        # change w proper error msg
        print("Cannot receive frame")
        break
    # pause the program for 15s after each frame
    time.sleep(15.0)

