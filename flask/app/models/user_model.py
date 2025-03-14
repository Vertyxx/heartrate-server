from flask_login import UserMixin
from app.__init__ import db


# Model User (Pacient i Lekar v jedné tabulce)
class User(db.Model, UserMixin):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    datum_narozeni = db.Column(db.Date, nullable=True)
    jmeno = db.Column(db.String(50), nullable=False)
    prijmeni = db.Column(db.String(50), nullable=False)
    narodnost = db.Column(db.String(50), default=None)
    titul = db.Column(db.String(20), default=None)
    email = db.Column(db.String(100), unique=True, nullable=False)
    heslo = db.Column(db.String(255), nullable=False)
    telefon = db.Column(db.String(20), default=None)
    role = db.Column(db.Enum('pacient', 'lekar', name="role_enum"), nullable=False)  # Určuje, zda je uživatel pacient nebo lékař
    zamereni = db.Column(db.String(100), default=None)  # Pouze pro lékaře (pacienti mají NULL)

    # Vztah M:N mezi pacienty a lékaři (pokud je user pacient, může mít lékaře a naopak)
    lekari = db.relationship('PacientLekar', foreign_keys='PacientLekar.pacient_id',
                             back_populates='pacient', cascade="all, delete-orphan", lazy="dynamic")

    pacienti = db.relationship('PacientLekar', foreign_keys='PacientLekar.lekar_id',
                               back_populates='lekar', cascade="all, delete-orphan", lazy="dynamic")

    # Vztah 1:N pro srdeční aktivitu (každý uživatel může mít vlastní záznamy)
    srdecni_aktivita = db.relationship('SrdecniAktivita', back_populates='uzivatel',
                                       cascade="all, delete-orphan", lazy="dynamic")



# Tabulka pro relaci mezi pacienty a lékaři (M:N)
class PacientLekar(db.Model):
    __tablename__ = 'Pacient_Lekar'

    pacient_id = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)
    lekar_id = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)
    stav = db.Column(db.Integer, default=0, nullable=False)  # 0 = pending, 1 = active, 2 = rejected, 3 = inactive

    pacient = db.relationship('User', foreign_keys=[pacient_id], back_populates='lekari')
    lekar = db.relationship('User', foreign_keys=[lekar_id], back_populates='pacienti')


# Model Srdecni_aktivita
class SrdecniAktivita(db.Model):
    __tablename__ = 'Srdecni_aktivita'

    uzivatel_id = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)
    cas = db.Column(db.DateTime, primary_key=True)
    cviceni = db.Column(db.Integer, default=0, nullable=False)  # 0 = žádná aktivita, 1 = lehká, 2 = střední, 3 = intenzivní
    bpm = db.Column(db.Float, nullable=False)

    uzivatel = db.relationship('User', back_populates='srdecni_aktivita')