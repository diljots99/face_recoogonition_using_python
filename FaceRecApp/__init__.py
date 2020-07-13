from flask import Flask
from  flask_sqlalchemy import  SQLAlchemy
from flask_bcrypt import  Bcrypt

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config["SERVER_NAME"] = "127.0.0.1:5000"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


from FaceRecApp import routes