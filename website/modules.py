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
        return f"<User {self.User_id}>"


class Project(db.Model):
    __tablename__ = 'Projects'
    
    Project_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    User_id = db.Column(db.Integer, db.ForeignKey('user.User_id'), nullable=False)
    name = db.Column(db.String(50), nullable=False, unique=True)
    voice_id = db.Column(db.Integer, db.ForeignKey('voices.voice_id'))
    quranversions_Version_id = db.Column(db.Integer, db.ForeignKey('quranversions.Version_id'), nullable=False)

    # ✅ Correct relationship
    quranversion = db.relationship('Quranversions', backref='projects')
    user = db.relationship('User', backref='projects')
    voice = db.relationship('Voices', backref='projects')

    
class Voices(db.Model):
    __tablename__ = 'voices'
    voice_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), unique = True, nullable = False)
    file_path = db.Column(db.VARCHAR(25),nullable = False)
    created_at = db.Column(db.Date, nullable=False, default=func.now())

class Quranversions(db.Model):
    __tablename__ = 'quranversions'
    Version_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), unique = True, nullable = False)
    language = db.Column(db.String(50), nullable = False)
    created_at = db.Column(db.Date, nullable=False, default=func.now())
    
    surahs = db.relationship('Surahs', backref='quran_version')
    
    def __repr__(self):
        return f"<QuranVersion {self.name} ({self.language})>"

class Surahs(db.Model):
    __tablename__ = 'surahs'
    
    sutrah_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    surah_number = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    arabic_name = db.Column(db.String(255), nullable=False)
    number_of_ayahs = db.Column(db.Integer, nullable=False)
    QuranVersions_Version_id = db.Column(db.Integer, db.ForeignKey('quranversions.Version_id'), nullable=False)
    
    # Relationship to Verses
    verses = db.relationship('Verses', backref='surah', lazy='dynamic')
    
    def __repr__(self):
        return f"<Surah {self.surah_number}: {self.name}>"
class Verses(db.Model):
    __tablename__ = 'verses'
    
    verse_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    verse_number = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)  # MEDIUMTEXT equivalent
    Surahs_sutrah_id = db.Column(db.Integer, db.ForeignKey('surahs.sutrah_id'), nullable=False)
    
    def __repr__(self):
        return f"<Verse {self.verse_number} of Surah {self.surah.surah_number}>"