from flask import Flask
from  flask_sqlalchemy import  SQLAlchemy
from flask_bcrypt import  Bcrypt
import os
from sqlalchemy_utils import database_exists

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config["SERVER_NAME"] = "127.0.0.1:5000"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from FaceRecApp import routes


path = str(os.path.realpath(__file__)).split("\\")
dbPath = "/".join(path[:-1]) + "/site.db"
print(dbPath)

if not os.path.exists(dbPath):
    db.create_all()
else:
    print("db Alredy exixts")
