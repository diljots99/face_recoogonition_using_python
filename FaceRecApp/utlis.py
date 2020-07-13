from FaceRecApp import db
from FaceRecApp.models import Persons


def getMaxID ():
    MaxIdQuery  = db.session.query(db.func.max(Persons.id)).scalar() 
    MaxIdUser = db.session.query(Persons).filter(Persons.id == MaxIdQuery).first()
    if MaxIdUser:
        ID = MaxIdUser.id + 1
    else:
        ID= 1
    
    return ID