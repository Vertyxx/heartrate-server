from flask_login import UserMixin
from app.__init__ import db

# Model Pacient
class Pacient(db.Model, UserMixin):
    __tablename__ = 'Pacient'
    
    id = db.Column(db.Integer, primary_key=True)
    datum_narozeni = db.Column(db.Date, nullable=False)
    jmeno = db.Column(db.String(50), nullable=False)
    prijmeni = db.Column(db.String(50), nullable=False)
    narodnost = db.Column(db.String(50), nullable=False)
    titul = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True, nullable=False)
    heslo = db.Column(db.String(255), nullable=False)
    telefon = db.Column(db.String(20))
    
    # Vztah M:N mezi pacienty a lékaři (přidán lazy="dynamic")
    lekari = db.relationship('PacientLekar', back_populates='pacient', cascade="all, delete-orphan", lazy="dynamic")

    # Vztah 1:N mezi pacientem a jeho srdeční aktivitou (přidán lazy="dynamic")
    srdecni_aktivita = db.relationship('SrdecniAktivita', back_populates='pacient', cascade="all, delete-orphan", lazy="dynamic")


# Model Lekar
class Lekar(db.Model, UserMixin):
    __tablename__ = 'Lekar'
    id = db.Column(db.Integer, primary_key=True)
    datum_narozeni = db.Column(db.Date, nullable=False)
    jmeno = db.Column(db.String(50), nullable=False)
    prijmeni = db.Column(db.String(50), nullable=False)
    narodnost = db.Column(db.String(50), nullable=False)
    zamereni = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    heslo = db.Column(db.String(255), nullable=False)
    telefon = db.Column(db.String(20))
    
    # Vztah M:N mezi lékaři a pacienty
    pacienti = db.relationship('PacientLekar', back_populates='lekar', cascade="all, delete-orphan", lazy="dynamic")


# Tabulka pro relaci mezi pacienty a lékaři (M:N)
class PacientLekar(db.Model):
    __tablename__ = 'Pacient_Lekar'
    
    pacient_id = db.Column(db.Integer, db.ForeignKey('Pacient.id'), primary_key=True)
    lekar_id = db.Column(db.Integer, db.ForeignKey('Lekar.id'), primary_key=True)
    stav = db.Column(db.Integer, default=0, nullable=False)  # 0 = pending, 1 = active, 2 = rejected, 3 = inactive

    pacient = db.relationship('Pacient', back_populates='lekari')
    lekar = db.relationship('Lekar', back_populates='pacienti')


# Model Srdecni_aktivita
class SrdecniAktivita(db.Model):
    __tablename__ = 'Srdecni_aktivita'

    pacient_id = db.Column(db.Integer, db.ForeignKey('Pacient.id'), primary_key=True)
    cas = db.Column(db.DateTime, primary_key=True)
    cviceni = db.Column(db.Integer, default=0, nullable=False)  
    bpm = db.Column(db.Float, nullable=False)

    pacient = db.relationship('Pacient', back_populates='srdecni_aktivita')