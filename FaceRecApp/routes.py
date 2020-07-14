import cv2,os,json,pprint

from flask import Flask, render_template, Response, request, flash, redirect, url_for,stream_with_context
from FaceRecApp import app,db,bcrypt

from  flask_sqlalchemy import  SQLAlchemy

from FaceRecApp.camera import VideoCamera

from FaceRecApp.Face_Functions import *
from FaceRecApp.forms import AddNewFace
from FaceRecApp.models import  Persons

from FaceRecApp.utlis import *

flag_start_capturing = False




@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


def gen(camera):
    while True:
        # get camera frame
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def capture(camera, username=None):
    print(username)
    try:
        person = Persons.query.filter_by(username=username).first()
        ID = person.id
        sample_dir_path = person.sample_dir_path
        print(person)
        no_of_samples = 0

        while no_of_samples < 20:

            frame, faces = camera.get_capture_frame()
            if faces is not None:
                basedir = os.getcwd().replace("\\", "/") + sample_dir_path
                if not os.path.exists(basedir):
                    os.makedirs(basedir)

                path = basedir + str(no_of_samples)+'.jpg'

                print(path)
                cv2.imwrite(path, faces[0])
                no_of_samples += 1
            cv2.putText(frame, "Samples Captured={}".format(no_of_samples), (5,
                        frame.shape[0] - 5), cv2.FONT_HERSHEY_PLAIN, 1.3, (66, 53, 243), 2, cv2.LINE_AA)
            ret, jpeg = cv2.imencode('.jpg', frame)

            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

        person.noOfSamples = no_of_samples
        db.session.commit()
        
        flash("Face Capture Succefully")
        redirect(url_for('index'))
    except :
        return None

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/capture_feed/<username>')
def capture_feed(username):
    print("capture_feed",username)
   
    feed = stream_with_context(capture(VideoCamera(), username))
    print("feed")
    res = Response(feed, mimetype='multipart/x-mixed-replace; boundary=frame')
    return res


@app.route('/add_new_face', methods=['GET', 'POST'])
def add_new_face_data():
    print(request.method)
  
    form = AddNewFace()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        ID =getMaxID()

        sample_dir_path = "/images/"+str(ID)+"/"

        print(form.gender.data)
         
        person = Persons(
            fullname= form.fullName.data,
            username= form.username.data,
            email=form.email.data,
            dob=form.dob.data,
            gender=form.gender.data,
            password=hashed_password,
            id=ID,
            sample_dir_path=sample_dir_path)

        
        db.session.add(person)
        db.session.commit()
        flash(f'Face data has been added,','success')
        return redirect(url_for("capture_face_data",username=form.username.data))

    return render_template('add_new_face.html',title="Add New Face", form=form)

    


@app.route('/capture_face_data/<username>')
def capture_face_data(username):
    print('heelo   '   ,username)
    return render_template('Capture_Face_Data.html',username=username)




@app.route("/start_training")
def start_traning():
    path = str(os.path.realpath(__file__)).split("\\")
    basePath= "/".join(path[:-2]) +"/images"
    print(basePath)
    print(os.path.exists(basePath))
    print(os.path.exists(basePath+"/hello"))

    if os.path.exists(basePath):
        numberOfClasses =  os.listdir(basePath)
        if len(numberOfClasses) < 2:
            flash("Add at least data of two faces Before starting Training","danger")
            return redirect(url_for("index"))
        else:
            status = train_model()
            if status:
                flash("Model Trained Succesfully","success")

            return redirect(url_for("index"))
    else:
        #TODO print Message add at least to faces
        print("print Message add at least to faces")
        flash("Add at least data of two faces Before starting Training","danger")
    
        return redirect(url_for("index"))
