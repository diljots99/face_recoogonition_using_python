import cv2

from tkinter import *
from Face_Functions import *

root = Tk()

vid = cv2.VideoCapture(0)



def draw_rectangle(image, coords):
    for (x, y, w, h) in coords:
        cv2.rectangle(image, (x , y), (x + w , y + h), (0,0,255),2)
while(True): 
      
    # Capture the video frame 
    # by frame 
    ret, frame = vid.read() 
  
    faces_coord = detect_face(frame)
    draw_rectangle(frame, faces_coord)
    print (faces_coord)

   

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