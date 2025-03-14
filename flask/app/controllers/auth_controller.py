from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user  # type: ignore
from werkzeug.security import check_password_hash, generate_password_hash  # type: ignore
from flask_sqlalchemy import SQLAlchemy  # type: ignore
from app import db
from app.models.user_model import User  # Použití nového modelu User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        heslo = request.form.get('password')

        # Hledání uživatele v databázi
        user = db.session.execute(db.select(User).filter_by(email=email)).scalar_one_or_none()

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
        role = request.form.get('role')  # 'pacient' nebo 'lekar'
        jmeno = request.form.get('jmeno')
        prijmeni = request.form.get('prijmeni')
        datum_narozeni = request.form.get('datum_narozeni')
        narodnost = request.form.get('narodnost')
        titul = request.form.get('titul')
        email = request.form.get('email')
        telefon = request.form.get('telefon')
        zamereni = request.form.get('zamereni') if role == 'lekar' else None  # Pouze pro lékaře
        heslo = request.form.get('password')
        heslo_confirm = request.form.get('password_confirm')

        if heslo != heslo_confirm:
            flash('Hesla se neshodují!', 'danger')
            return redirect(url_for('auth.register'))

        # Kontrola, zda už uživatel existuje
        existing_user = db.session.execute(db.select(User).filter_by(email=email)).scalar_one_or_none()

        if existing_user:
            flash('Účet s tímto e-mailem již existuje!', 'danger')
            return redirect(url_for('auth.register'))

        # Hashování hesla
        hashed_heslo = generate_password_hash(heslo, method='pbkdf2:sha256')

        # Vytvoření nového uživatele
        new_user = User(
            jmeno=jmeno,
            prijmeni=prijmeni,
            datum_narozeni=datum_narozeni,
            narodnost=narodnost,
            titul=titul,
            email=email,
            heslo=hashed_heslo,
            telefon=telefon,
            role=role,
            zamereni=zamereni  # Bude None pro pacienty
        )

        # Uložení uživatele do databáze
        with db.session.begin():
            db.session.add(new_user)

        flash('Registrace byla úspěšná! Nyní se můžete přihlásit.', 'success')
        return redirect(url_for('auth.login'))

    return render_template("register.html")


@auth.route('/logout')
def logout():
    logout_user()
    flash("Byl jsi úspěšně odhlášen.", "success")
    return redirect(url_for('main.homepage'))