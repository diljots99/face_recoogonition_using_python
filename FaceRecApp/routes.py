import cv2,os,json,pprint

from flask import Flask, render_template, Response, request, flash, redirect, url_for
from FaceRecApp import app

from  flask_sqlalchemy import  SQLAlchemy

from FaceRecApp.camera import VideoCamera

from FaceRecApp.Face_Functions import *
from FaceRecApp.forms import AddNewFace
from FaceRecApp.models import  Persons



flag_start_capturing = False




# db = MyDatabase()



@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


def gen(camera):
    while True:
        # get camera frame
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def capture(camera, form=None):
    ID = db.get_new_insert_id("peoples")
    sample_dir_path = "/images/"+str(ID)+"/"
    print(form)
    print(type(form))
    userData = eval(str(form))
    userData["_id"] = ID
    userData['sample_dir_path'] = sample_dir_path
    print(userData)

    samples = []
    no_of_samples = 0

    while no_of_samples < 20:

        frame, faces = camera.get_capture_frame()
        if faces is not None:
            basedir = os.getcwd().replace("\\", "/") + sample_dir_path
            if not os.path.exists(basedir):
                os.makedirs(basedir)

            path = basedir + str(no_of_samples)+'.jpg'

            samples.append(sample_dir_path+str(no_of_samples)+'.jpg')
            print(path)

            cv2.imwrite(path, faces[0])
            no_of_samples += 1

        cv2.putText(frame, "Samples Captured={}".format(no_of_samples), (5,
                    frame.shape[0] - 5), cv2.FONT_HERSHEY_PLAIN, 1.3, (66, 53, 243), 2, cv2.LINE_AA)
        ret, jpeg = cv2.imencode('.jpg', frame)

        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

    userData["samples"] = samples
    db.insert_user_data("peoples", userData)
    with app.app_context():
        redirect(url_for("index"))


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/capture_feed/<form>')
def capture_feed(form):
    feed = capture(VideoCamera(), form)
    if feed == None:
       pass
    res = Response(feed, mimetype='multipart/x-mixed-replace; boundary=frame')

    return res


@app.route('/add_new_face', methods=['GET', 'POST'])
def add_new_face_data():
    print(request.method)
  
    form = AddNewFace()
    if form.validate_on_submit():
        Form = dict(request.form)
        data = json.dumps(Form)
        flash(f'Account Data Gathered','success')
        return redirect(url_for("capture_face_data",form=data))
    return render_template('add_new_face.html',title="Add New Face", form=form)

    


@app.route('/capture_face_data/<form>')
def capture_face_data(form):
    print('heelo   '   ,form)
    return render_template('Capture_Face_Data.html',form=form)




@app.route("/start_training")
def start_traning():
    train_model()
    return redirect(url_for("index"))
