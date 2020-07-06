import cv2

from tkinter import *
from Face_Functions import *
import numpy as np
from PIL import Image, ImageTk

root = Tk()

vid = cv2.VideoCapture(0)



def live_Capture():

    while(True): 


        # Capture the video frame 
        # by frame 
        ret, frame = vid.read() 
    
        faces_coord = detect_face(frame)
        draw_rectangle(frame, faces_coord)
        if len(faces_coord):
            detect_gender(frame,faces_coord)
        print (faces_coord)

        #TODO predict if face exixts 

        if False:
            #TODO  when face already exists in database show the relatcent atributes
            pass
        else:
            pass

        # Display the resulting frame 
        cv2.imshow('frame', frame) 

        # the 'q' button is set as the 
        # quitting button you may use any 
        # desired button of your choice 
        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break


    # After the loop release the cap object 
    vid.release() 
    # Destroy all the windows 
    cv2.destroyAllWindows() 

def Add_face():
        
    vid = cv2.VideoCapture(0)
    #cv2.namedWindow("Face", cv2.WINDOW_AUTOSIZE)
    ret, frame = vid.read() 
    ad = cv2.imshow('frame', frame) 

live_Capture()