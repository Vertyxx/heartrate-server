import os

class Config:
    DEBUG = True 

    # DB_USERNAME = os.getenv("DB_USERNAME", "uzivatel")  # Hodnota z docker-compose.yml
    # DB_PASSWORD = os.getenv("DB_PASSWORD", "heslo")
    # DB_HOST = os.getenv("DB_HOST", "mariadb")  # Název služby v Docker Compose
    # DB_NAME = os.getenv("DB_NAME", "HeartRate")

    # SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}"

    DB_USERNAME = os.getenv("DB_USERNAME", "root")  # Defaultně použije "root"
    DB_PASSWORD = os.getenv("DB_PASSWORD", "root")  # Defaultně použije "root"
    DB_HOST = os.getenv("DB_HOST", "147.228.64.42")  # IP adresa databáze
    DB_NAME = os.getenv("DB_NAME", "HeartRate")  # Název databáze

    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:3306/{DB_NAME}"


    # Zakázání sledování změn objektů pro lepší výkon
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = os.getenv("SECRET_KEY", "a") 

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "supertajnyklic")  # Načte JWT klíč z Docker proměnné
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # Token platný 1 hodinu
    JWT_ALGORITHM = "HS256"  # Nebo "HS512"
