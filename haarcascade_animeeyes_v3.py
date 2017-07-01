import cv2
import numpy as np
import os
animeeye=cv2.imread(os.getcwd()+'/images/Anime_eye.png')
animeeye=cv2.resize(animeeye,None,fx=0.05,fy=0.05,interpolation=cv2.INTER_CUBIC)
##################################################################################
#haar cascades from https://github.com/opencv/opencv/tree/master/data/haarcascades
face_cascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade=cv2.CascadeClassifier('haarcascade_eye.xml')
##################################################################################

cap=cv2.VideoCapture(0)

while True:
    savevid=raw_input('Would you like to save the video? (y/n)')
    if (savevid.lower()=='y') or (savevid.lower()=='yes'):
        fourcc=cv2.cv.CV_FOURCC(*'XVID')
        out=cv2.VideoWriter('kawaii.avi',fourcc,20.0,(640,480))
        break
    elif savevid.lower()=='n' or (savevid.lower()=='no'):
        break
    else:
        print 'Invalid input.  Please type y or n.'
        
while True:
    ret,img=cap.read()
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces=face_cascade.detectMultiScale(gray,1.3,5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray=gray[y:y+h,x:x+w]
        roi_gray_half=gray[y:y+h/2,x:x+w]
        roi_color=img[y:y+h,x:x+w]
        eyes=eye_cascade.detectMultiScale(roi_gray_half)
        
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
            dst=img
            dst[ey+y:ey+y+animeeye.shape[0],ex+x:ex+x+animeeye.shape[1],:]=animeeye

    try:
        cv2.imshow('img',dst)
    except:
        cv2.imshow('img',img)
    if (savevid.lower()=='y') or (savevid.lower()=='yes'):
        try:
            out.write(dst)
        except:
            print 'ERROR on writing to file'
    k=cv2.waitKey(30) & 0xff
    if k==27:
        break

cap.release()
if (savevid.lower()=='y') or (savevid.lower()=='yes'):
    out.release()
cv2.destroyAllWindows()
