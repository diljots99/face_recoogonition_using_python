import cv2
# defining face detector
face_cascade=cv2.CascadeClassifier("xml/frontal_face.xml")
ds_factor=1.0
from FaceRecApp.Face_Functions import *
from datetime import date
from FaceRecApp.models import  Persons
from FaceRecApp import db


class VideoCamera(object):
    def __init__(self):
       #capturing video
       self.video = cv2.VideoCapture(0)    
    
    def __del__(self):
        #releasing camera
        self.video.release()
    
   
    def get_frame(self):
       #extracting frames
        ret, frame = self.video.read()
        frame=cv2.resize(frame,None,fx=ds_factor,fy=ds_factor, interpolation=cv2.INTER_AREA)                    
        
        # gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        faces_coord = detect_face(frame)

        if len(faces_coord):
           
            basedir = os.getcwd().replace("\\","/") +"/models"
            if os.path.exists(basedir):
                try:
                    ID = predict(frame,faces_coord)
                except :
                    print("Exception Occred in Prediction")

                try:    
                    person = Persons.query.get(ID)
                    name = person.fullname
                    dob = person.dob
                    gender = person.gender
                    
                except :
                    print("Unable To fetch Predicted id from db")
                    name,age,gender = ""
                   
                try:
                    age = calculate_age(dob)
                except :
                    print("exception occured in calculating age")
                    age = ""

                   
                info = str(name) + " "+ str(age) +" "+str(gender)
                cv2.putText(frame, info,(faces_coord[0][0], faces_coord[0][1] - 10),
                        cv2.FONT_HERSHEY_PLAIN, 2, (66, 53, 243), 2)
                draw_rectangle(frame, faces_coord)
               
                # detect_gender(frame,faces_coord)
                # draw_rectangle(frame, faces_coord)

            else:
                detect_gender(frame,faces_coord)
                draw_rectangle(frame, faces_coord)

        # face_rects=face_cascade.detectMultiScale(gray,1.3,5)

        # for (x,y,w,h) in face_rects:
        #  cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        #  break

      
        # encode OpenCV raw frame to jpg and displaying it
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def get_capture_frame(self):
            ret, frame = self.video.read()
            frame=cv2.resize(frame,None,fx=ds_factor,fy=ds_factor, interpolation=cv2.INTER_AREA)                    
            
            faces_coord = detect_face(frame)

            if len(faces_coord):
                faces = normalize_faces(frame,faces_coord)
                draw_rectangle(frame,faces_coord)
            else:
                faces = None
                
            
           
            
            return frame,faces
