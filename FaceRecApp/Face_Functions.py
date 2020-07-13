import cv2
import os
import numpy as np
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC,LinearSVC
from sklearn.model_selection import GridSearchCV,KFold
import pickle
# from FaceRecApp.database import MyDatabase
from datetime import date,datetime

def detect_face(frame):
    detector = cv2.CascadeClassifier("FaceRecApp/xml/frontal_face.xml")
    faces = detector.detectMultiScale(frame,1.2)
    return faces

def draw_rectangle(image, coords):
    for (x, y, w, h) in coords:
        cv2.rectangle(image, (x , y), (x + w , y + h), (0,0,255),2)

def detect_gender(frame,faces):

    genderProto="FaceRecApp/detectionModel/gender_deploy.prototxt"
    genderModel="FaceRecApp/detectionModel/gender_net.caffemodel"
    genderList=['Male','Female']
    MODEL_MEAN_VALUES=(78.4263377603, 87.7689143744, 114.895847746)
    genderNet=cv2.dnn.readNet(genderModel,genderProto)
    
    ageProto="FaceRecApp/detectionModel/age_deploy.prototxt"
    ageModel="FaceRecApp/detectionModel/age_net.caffemodel"
    ageNet=cv2.dnn.readNet(ageModel,ageProto)
    ageList=['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
    padding=20
    genderAGE = []
    for i, faceBox in enumerate(faces):
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
            
            cv2.putText(frame, str (gender)+" "+str(age[1:-1]),(faces[i][0], faces[i][1] - 10),
                        cv2.FONT_HERSHEY_PLAIN, 2, (66, 53, 243), 2)
            genderAGE.append([gender,age[1:-1]])
        except :
            pass
    return genderAGE


def cut_faces(image, faces_coord):
    faces = []
    for (x, y, w, h) in faces_coord:
        faces.append(image[y: y + h, x : x + w ])
    return faces

def normalize_intensity(images):
    images_norm = []
    for image in images:
        images_norm.append(cv2.equalizeHist(image))
    return images_norm

def resize(images,size=(47,62)):
    image_resize = []
    
    for image in images:
        img_size = cv2.resize(image,size)
        
        image_resize.append(img_size)
        
    return image_resize


def normalize_faces(frame, faces_coord):
    #gray_frame = gray_scale(frame)
    faces = cut_faces(frame, faces_coord)
    # faces = normalize_intensity(faces)
    
    faces = resize(faces)
    return faces

def collect_dataset():
    images = []
    labels = []
    labels_dic = {}
   
    people = [person for person in os.listdir("images/")]
   
    for i, person in enumerate(people):
        labels_dic[i] = person
        for image in os.listdir("images/" + person):
            if image.endswith('.jpg'):
                images.append(cv2.imread("images/" + person + '/' + image, 0))
                labels.append(i)
    return (images, np.array(labels), labels_dic)


def train_model():
    images, labels, labels_dic = collect_dataset()
    print(images)
    print(labels)
    print(labels_dic)
    X_train=np.asarray(images)
    train=X_train.reshape(len(X_train),-1)
    
    sc = StandardScaler()
    X_train_sc = sc.fit_transform(train.astype(np.float64))
    
    pca1 = PCA(n_components=.97)
    new_train=pca1.fit_transform(X_train_sc)
    kf=KFold(n_splits=5,shuffle=True)
    param_grid = {'C':[.0001,.001,.01,.1,1,10]}
    gs_svc = GridSearchCV(SVC(kernel='linear',probability=True),param_grid=param_grid,cv=kf,scoring='accuracy')

    gs_svc.fit(new_train,labels)
    svc1=gs_svc.best_estimator_

    basedir = os.getcwd().replace("\\","/") +"/models"
    print(basedir)
    
    if not os.path.exists(basedir):
        os.makedirs(basedir)

    filename = '/svc_linear_face.pkl'
    f=open(basedir+filename, 'wb')
    pickle.dump(svc1,f)
    f.close()

    filename = '/pca.pkl'
    f=open(basedir+filename, 'wb')
    pickle.dump(pca1,f)
    f.close()

    filename = '/standardscalar.pkl'
    f=open(basedir+filename, 'wb')
    pickle.dump(sc,f)
    f.close()
    print('model has been trained')
    return True


def predict(frame,faces_coord):
    global label
    images, labels, labels_dic = collect_dataset()

    basedir = os.getcwd().replace("\\","/") +"/models"
    print(basedir)

    filename = '/svc_linear_face.pkl'
    svc1 = pickle.load(open(basedir+filename, 'rb'))

    filename = '/pca.pkl'
    pca1 = pickle.load(open(basedir+filename, 'rb'))

    filename = '/standardscalar.pkl'
    sc = pickle.load(open(basedir+filename, 'rb'))

    if len(faces_coord):
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = normalize_faces(gray, faces_coord)
         
        for i, face in enumerate(faces): # for each detected face
            t=face.reshape(1,-1)
            t=sc.transform(t.astype(np.float64))
            test = pca1.transform(t)    
        
            prob=svc1.predict_proba(test)
            confidence = svc1.decision_function(test)
            print (confidence)
            print (prob)
        
        
        
            pred = svc1.predict(test)
            print (pred,pred[0])
        
            name=pred
            print (name)
            ID = int(labels_dic[pred[0]])
            
        
        draw_rectangle(frame, faces_coord) # rectangle around face
        
        return ID
    else:
        return None
        

def calculate_age(birthdate):
    birthDateObj  = birthdate
    today = date.today()
    print(birthdate)
    print(birthDateObj)
    # age = today.year - birthDateObj.year - ((today.month, today.day) <  (birthDateObj.month, birthDateObj.day)) 
    days_in_YEAR = 365.2425
    age = int((today - birthDateObj).days/days_in_YEAR)

    print(age)
    return age