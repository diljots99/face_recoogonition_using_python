# import the necessary packages
import cv2
# defining face detector
face_cascade=cv2.CascadeClassifier("xml/frontal_face.xml")
ds_factor=1.0
from Face_Functions import *

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

        draw_rectangle(frame, faces_coord)
        if len(faces_coord):
            detect_gender(frame,faces_coord)

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
                # faces = normalize_faces(frame,faces_coord)
                isFaceCaputred = True
            else:
                isFaceCaputred =False
                
            
           
            
            return frame,isFaceCaputred
