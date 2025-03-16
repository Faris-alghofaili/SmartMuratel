from . import db
from flask_login import UserMixin
from datetime import datetime , date
from sqlalchemy import ForeignKeyConstraint, PrimaryKeyConstraint, func
from sqlalchemy.dialects.mysql import TINYTEXT




class User(db.Model,UserMixin):
    __tablename__ = 'user'
    User_id = db.Column(db.Integer, primary_key=True, )
    first_name = db.Column(db.String(50), nullable=False)
    Username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)  # Changed TINYTEXT to Text for better compatibility
    is_admin = db.Column(db.Boolean, nullable=False)  # Changed TINYINT to Boolean
    created_at = db.Column(db.Date, nullable=False, default=func.now())
     # ✅ Override get_id() to return User_id
    def get_id(self):
        return str(self.User_id)

    def __repr__(self):
        return f"<User {self.Username}>"

class Projects(db.Model):
    __tablename__ = 'projects'
    Project_id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(50),unique = True,nullable = False)
    id = db.Column(db.Integer, db.ForeignKey('user.id'))
    version_id = db.Column(db.Integer, db.ForeignKey('quranversions.Version_id'))
    voice_id = db.Column(db.Integer, db.ForeignKey("voices.voice_id"))


class Quranversions(db.Model):
    __tablename__ = 'quranversions'
    Version_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), unique = True, nullable = False)
    langaue = db.Column(db.String(50), nullable = False)
    created_at = db.Column(db.Date, nullable=False, default=func.now())

class Voices(db.Model):
    __tablename__ = 'voices'
    voice_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), unique = True, nullable = False)
    file_path = db.Column(db.VARCHAR(25),nullable = False)
    created_at = db.Column(db.Date, nullable=False, default=func.now())




