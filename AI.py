import cv2
import os
import time
import numpy
import email, smtplib, ssl
import tweepy
import datetime
from autoEmail import *

# retrieve email info from text file
file = open('userInfo.txt', 'r')
lines = file.readlines()
sysEmail = lines[1]
recEmail = lines[3]
pword = lines[5]
twitterAccessKey = lines[7]
twitterSecretKey = lines[9]
# close text file
file.close()

# fill in "access" and "secret" w twitter development keys
auth = tweepy.OAuthHandler(twitterAccessKey, twitterSecretKey)
# access the twitter account
auth.set_access_token(,)
# get our wrapped Twitter API
api = tweepy.API(auth)

# turn on camera
camera = cv2.VideoCapture(0)
# if camera is off, exit program
if not camera.isOpened():
    # send email if camera is off
    sendEmail("Camera is off", recEmail, sysEmail, pword, "Alert")
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
            # draw rectangle around predator faces
            for (x,y,w,h) in predators:
                cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), thickness=1)
            # alert farmer of predator via email
            cv2.imwrite('predator.jpg', img)
            now = getTime()
            sendEmail("Predator Alert at ${now}", recEmail, sysEmail, pword, 'predator.jpg', "Alert")
            # tweet an image of predator in pen
            api.update_with_media('predator.jpg', "In the pen at ${now}")
            # delete recently produced .jpg
            os.remove('predator.jpg')
        if len(humans) > 0:
            # draw rectangle around humans
            for (x,y,w,h) in humans:
                cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), thickness=1)
             # alert farmer of humans via email
            cv2.imwrite('human.jpg', img)
            now = getTime()
            sendEmail("Intruder Alert at ${now}", recEmail, sysEmail, pword, 'human.jpg', "Alert")
             # tweet an image of person in pen
            api.update_with_media('human.jpg', "In the pen at ${now}")
            # delete recently produced .jpg
            os.remove('human.jpg')
    else:
        # send error msg in email
        sendEmail("ERROR: Camera is not working", recEmail, sysEmail, pword, "Alert")
        break
    # pause the program for 60s after each frame
    time.sleep(60)
# send email if camera is off and exit program
sendEmail("Camera is off", recEmail, sysEmail, pword, "Alert")
exit()
