from cv2 import cv2
import os,urllib.request
import numpy as np
from django.conf import settings
from django.http.response import StreamingHttpResponse
from django.contrib import messages
import dlib
import sys

camera = cv2.VideoCapture(0)
haar_file = 'static/haarcascade_frontalface_default.xml'
datasets = 'static/datasets'

def face_recognize():
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
    i=0
    while True:
        success,frame=camera.read()
        if not success:
            break
        else:
            # Part 1: Create fisherRecognizer 
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            if len(faces) == 0:
                i=i+1
                if i%1==0:
                    print("warn",i/500)
                    j=500
                    while j>0:
                        j=j-1
                        cv2.putText(frame, 'warning',(50, 150), cv2.FONT_HERSHEY_PLAIN, 10, (0, 0, 255))
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2) 
                face = gray[y:y + h, x:x + w] 
                face_resize = cv2.resize(face, (width, height)) 
                # Try to recognize the face
                prediction = model.predict(face_resize) 
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
                
                if prediction[1]<70:
                    cv2.putText(frame, '% s - %.0f' %(names[prediction[0]], prediction[1]), (x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
                else:
                    cv2.putText(frame, 'not recognized',(x-10, y-10),cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 0))
                    i=i+1
                    if i%1==0:
                        print("warn",i/500)
                        j=500
                        while j>0:
                            j=j-1
                            cv2.putText(frame, 'warning',(x, y), cv2.FONT_HERSHEY_PLAIN, 10, (0, 0,255))
            cv2.imshow('OpenCV', frame)
            key = cv2.waitKey(10)
            if key == 27:
                break



def gen_frames(p):
    while True:
        #capture frame by frame
        success,frame=camera.read()
        if not success:
            break
        else:
            sub_data = p
            path = os.path.join(datasets, sub_data)
            if not os.path.isdir(path):
                os.mkdir(path)
            (width, height) = (130, 100)
            face_cascade = cv2.CascadeClassifier(haar_file) 
            # webcam = cv2.VideoCapture(0)
            count = 1
            while count < 5:
                (_, im) = camera.read()
                faces = face_cascade.detectMultiScale(im, 1.3, 6)
                for (x, y, w, h) in faces:
                    cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    face = im[y:y + h, x:x + w]
                    face_resize = cv2.resize(face, (width, height))
                    cv2.imwrite('% s/% s.png' % (path, count), face_resize)
                count += 1
                print(count)
                if count==5:
                    resize = cv2.resize(frame,(1000,530),interpolation=cv2.INTER_LINEAR)
                    frame_flip=cv2.flip(resize,1)
                    _,buffer=cv2.imencode('.jpg',frame_flip)
                    frame=buffer.tobytes()
                    yield(b'--frame\r\n'
			                b'Content-Type:image/jpeg\r\n\r\n'+ frame + b'\r\n')
            camera.release
            face_recognize()



