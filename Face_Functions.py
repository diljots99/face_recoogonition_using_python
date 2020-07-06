import cv2
import os
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC,LinearSVC
from sklearn.model_selection import GridSearchCV,KFold
import pickle


def detect_face(frame):
    detector = cv2.CascadeClassifier("xml/frontal_face.xml")
    faces = detector.detectMultiScale(frame,1.2)
    return faces

def draw_rectangle(image, coords):
    for (x, y, w, h) in coords:
        cv2.rectangle(image, (x , y), (x + w , y + h), (0,0,255),2)

def detect_gender(frame,faces):

    genderProto="detectionModel/gender_deploy.prototxt"
    genderModel="detectionModel/gender_net.caffemodel"
    genderList=['Male','Female']
    MODEL_MEAN_VALUES=(78.4263377603, 87.7689143744, 114.895847746)
    genderNet=cv2.dnn.readNet(genderModel,genderProto)
    
    ageProto="detectionModel/age_deploy.prototxt"
    ageModel="detectionModel/age_net.caffemodel"
    ageNet=cv2.dnn.readNet(ageModel,ageProto)
    ageList=['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
    padding=20
    for faceBox in faces:
        face=frame[max(0,faceBox[1]-padding):
                   min(faceBox[3]+padding,frame.shape[0]-1),max(0,faceBox[0]-padding)
                   :min(faceBox[2]+padding, frame.shape[1]-1)]
        try:
           
            blob=cv2.dnn.blobFromImage(face, 1.0, (227,227), MODEL_MEAN_VALUES, swapRB=False)
            genderNet.setInput(blob)
            genderPreds=genderNet.forward()
            gender=genderList[genderPreds[0].argmax()]
            print(f'Gender: {gender}')

            ageNet.setInput(blob)
            agePreds=ageNet.forward()
            age=ageList[agePreds[0].argmax()]
            print(f'Age: {age[1:-1]} years')
        except :
            pass