import os

# Použití proměnné prostředí, pokud existuje, jinak fallback na defaultní hodnotu
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mysql+pymysql://uzivatel:heslo@localhost:3306/HeartRate")

# Zakázání sledování změn objektů pro lepší výkon
SQLALCHEMY_TRACK_MODIFICATIONS = False
class Config:
    DEBUG = True 