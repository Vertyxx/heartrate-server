from flask_login import UserMixin
from app.__init__ import db

# Model Pacient
class Pacient(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    datum_narozeni = db.Column(db.Date, nullable=False)
    jmeno = db.Column(db.String(50), nullable=False)
    prijmeni = db.Column(db.String(50), nullable=False)
    narodnost = db.Column(db.String(50), nullable=False)
    titul = db.Column(db.String(20))
    email = db.Column(db.String(100), unique=True, nullable=False)
    heslo = db.Column(db.String(100), nullable=False)
    telefon = db.Column(db.String(20))
    
    # Vztah M:N mezi pacienty a lékaři
    lekari = db.relationship('PacientLekar', back_populates='pacient', cascade="all, delete-orphan")

    # Vztah 1:N mezi pacientem a jeho srdeční aktivitou
    srdecni_aktivita = db.relationship('SrdecniAktivita', back_populates='pacient', cascade="all, delete-orphan")


# Model Lekar
class Lekar(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    datum_narozeni = db.Column(db.Date, nullable=False)
    jmeno = db.Column(db.String(50), nullable=False)
    prijmeni = db.Column(db.String(50), nullable=False)
    narodnost = db.Column(db.String(50), nullable=False)
    zamereni = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    heslo = db.Column(db.String(100), nullable=False)
    telefon = db.Column(db.String(20))
    
    # Vztah M:N mezi lékaři a pacienty
    pacienti = db.relationship('PacientLekar', back_populates='lekar', cascade="all, delete-orphan")


# Tabulka pro relaci mezi pacienty a lékaři (mnoho na mnoho)
class PacientLekar(db.Model):
    pacient_id = db.Column(db.Integer, db.ForeignKey('pacient.id'), primary_key=True)
    lekar_id = db.Column(db.Integer, db.ForeignKey('lekar.id'), primary_key=True)

    pacient = db.relationship('Pacient', back_populates='lekari')
    lekar = db.relationship('Lekar', back_populates='pacienti')


# Model Srdecni_aktivita
class SrdecniAktivita(db.Model):
    pacient_id = db.Column(db.Integer, db.ForeignKey('pacient.id'), primary_key=True)
    cas = db.Column(db.DateTime, primary_key=True)
    cviceni = db.Column(db.Integer, default=0, nullable=False)  # 0 - žádné, 1 - lehké, 2 - střední, 3 - intenzivní
    bpm = db.Column(db.Float, nullable=False)

    pacient = db.relationship('Pacient', back_populates='srdecni_aktivita')