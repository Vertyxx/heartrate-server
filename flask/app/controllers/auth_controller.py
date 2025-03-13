from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user     # type: ignore
from werkzeug.security import check_password_hash, generate_password_hash   # type: ignore
from flask_sqlalchemy import SQLAlchemy     # type: ignore
from app import db
from app.models.user_model import Pacient, Lekar

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        heslo = request.form.get('password')

        # Dotaz na uživatele v SQLAlchemy
        user = db.session.execute(db.select(Pacient).filter_by(email=email)).scalar_one_or_none()
        if not user:
            user = db.session.execute(db.select(Lekar).filter_by(email=email)).scalar_one_or_none()

        if user and check_password_hash(user.heslo, heslo):
            login_user(user)
            flash('Úspěšné přihlášení', 'success')
            return redirect(url_for('main.homepage'))
        else:
            flash('Neplatné přihlašovací údaje', 'danger')

    return render_template("login.html")


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        role = request.form.get('role')
        jmeno = request.form.get('jmeno')
        prijmeni = request.form.get('prijmeni')
        datum_narozeni = request.form.get('datum_narozeni')
        narodnost = request.form.get('narodnost')
        titul = request.form.get('titul')
        email = request.form.get('email')
        telefon = request.form.get('telefon')
        zamereni = request.form.get('zamereni')  # Pouze pro lékaře

        heslo = request.form.get('password')
        heslo_confirm = request.form.get('password_confirm')

        if heslo != heslo_confirm:
            flash('Hesla se neshodují!', 'danger')
            return redirect(url_for('auth.register'))

        with db.session.begin():  # Ujistíme se, že dotazy na databázi jsou správně propojené
            existing_user = db.session.execute(db.select(Pacient).filter_by(email=email)).scalar_one_or_none()
            if not existing_user:
                existing_user = db.session.execute(db.select(Lekar).filter_by(email=email)).scalar_one_or_none()

        if existing_user:
            flash('Účet s tímto e-mailem již existuje!', 'danger')
            return redirect(url_for('auth.register'))

        hashed_heslo = generate_password_hash(heslo, method='pbkdf2:sha256')

        if role == 'pacient':
            new_user = Pacient(
                jmeno=jmeno,
                prijmeni=prijmeni,
                datum_narozeni=datum_narozeni,
                narodnost=narodnost,
                titul=titul,
                email=email,
                heslo=hashed_heslo,
                telefon=telefon
            )
        elif role == 'lekar':
            new_user = Lekar(
                jmeno=jmeno,
                prijmeni=prijmeni,
                datum_narozeni=datum_narozeni,
                narodnost=narodnost,
                zamereni=zamereni,  # Speciální pole pro lékaře
                email=email,
                heslo=hashed_heslo,
                telefon=telefon
            )
        else:
            flash('Neplatná role!', 'danger')
            return redirect(url_for('auth.register'))

        with db.session.begin():  # Použití správného kontextu pro uložení
            db.session.add(new_user)

        flash('Registrace byla úspěšná! Nyní se můžete přihlásit.', 'success')
        return redirect(url_for('auth.login'))

    return render_template("register.html")

@auth.route('/logout')
def logout():
    logout_user()
    flash("Byl jsi úspěšně odhlášen.", "success")
    return redirect(url_for('main.homepage')) 