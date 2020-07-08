from flask import Flask, render_template, Response,request,flash,redirect,url_for
from camera import VideoCamera
import  cv2
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

flag_start_capturing = False


@app.route('/',methods=['GET', 'POST'])
def index():
   
    return render_template('index.html')

def gen(camera):
    while True:
        #get camera frame
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def capture(camera):
    no_of_samples=0
    while True:
        
        #get camera frame
        frame,isFaceCaputred = camera.get_capture_frame()
        if isFaceCaputred:
            no_of_samples += 1
        cv2.putText(frame, "Samples Captured={}".format(no_of_samples), (5, frame.shape[0] - 5),cv2.FONT_HERSHEY_PLAIN, 1.3, (66, 53, 243), 2,cv2.LINE_AA)    
        ret, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture_feed')
def capture_feed():
    return Response(capture(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/add_new_face',methods=['GET', 'POST'])
def add_new_face_data():
    print(request.method)
    if request.method == 'POST':
        Form  = dict(request.form)
        print(Form['fullName'])
        print(Form['age'])
        print(Form['gender'])
        return redirect(url_for("capture_face_data",form=Form))
    return render_template('add_new_face.html')


@app.route('/capture_face_data/<form>')
def capture_face_data(form):
    print('heelo   '   ,form)
    # print(form.get('fullName'))
    # print(form.get('age'))
    # print(form.get('gender'))
    return render_template('Capture_Face_Data.html')


if __name__ == '__main__':
    # defining server ip address and port
    app.run(port='5000', debug=True)