from cv2 import cv2
import os,urllib.request
import numpy as np
from django.conf import settings
from django.http.response import StreamingHttpResponse
from django.contrib import messages
# import dlib
import sys

size = 4
print("WEart1")
haar_file = 'static/haarcascade_frontalface_default.xml'
print("WEart4")
datasets = 'static/datasets'

camera = cv2.VideoCapture(0)

def face_recognize():
    print('Recognizing Face Please Be in sufficient Lights...')
    # Create a list of images and a list of corresponding names
    (images, lables, names, id) = ([], [], {}, 0)
    for (subdirs, dirs, files) in os.walk(datasets):
        for subdir in dirs:
            names[id] = subdir
            subjectpath = os.path.join(datasets, subdir)
            for filename in os.listdir(subjectpath):
                path = subjectpath + '/' + filename
                lable = id
                images.append(cv2.imread(path, 0))
                lables.append(int(lable))
            id += 1
    (width, height) = (130, 100)
    # Create a Numpy array from the two lists above
    (images, lables) = [np.array(lis) for lis in [images, lables]]
    # OpenCV trains a model from the images
    # NOTE FOR OpenCV2: remove '.face'
    model = cv2.face.LBPHFaceRecognizer_create()
    model.train(images, lables)
    # Part 2: Use fisherRecognizer on camera stream
    face_cascade = cv2.CascadeClassifier(haar_file)
    
    while True:
        print("WEart")
        success,frame=camera.read()
        print("WEart2")
        if not success:
            print("WEart3")
            break
        else:
            # Part 1: Create fisherRecognizer 
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2) 
                face = gray[y:y + h, x:x + w] 
                face_resize = cv2.resize(face, (width, height)) 
                # Try to recognize the face
                prediction = model.predict(face_resize) 
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                
                if prediction[1]<500:
                    cv2.putText(frame, '% s - %.0f' %(names[prediction[0]], prediction[1]), (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
                else:
                    cv2.putText(frame, 'not recognized',cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2))
                face = gray[y:y + h, x:x + w]
                face_resize = cv2.resize(face, (width, height))
                # Try to recognize the face
                prediction = model.predict(face_resize)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                
                if prediction[1]<500:
                    (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0)
            cv2.imshow('OpenCV', frame)
            key = cv2.waitKey(10)
            if key == 27:
                break



