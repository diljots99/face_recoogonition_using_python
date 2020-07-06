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
