from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user        # type: ignore
from app import db
from app.models.user_model import SrdecniAktivita, User, PacientLekar

main = Blueprint('main', __name__)

@main.route("/")
@login_required
def homepage():
    # Získání srdeční aktivity pro aktuálního uživatele (pacienta i lékaře)
    aktivity = (
        db.session.query(SrdecniAktivita.cas, SrdecniAktivita.bpm)
        .filter(SrdecniAktivita.uzivatel_id == current_user.id)
        .order_by(SrdecniAktivita.cas.asc())
        .all()
    )

    # Převod dat na seznamy pro JSON
    casove_razitka = [a.cas.strftime("%Y-%m-%d %H:%M:%S") for a in aktivity]  # Formát času
    hodnoty_srdce = [a.bpm for a in aktivity]  # BPM hodnoty

    return render_template(
        "homepage.html",
        casove_razitka=casove_razitka,
        hodnoty_srdce=hodnoty_srdce
    )


#zatim to necham tady, popr nezapon vyhodit importy: redirect, url_for, flash
@main.route("/moji-pacienti")
@login_required
def moji_pacienti():
    if current_user.role != "lekar":
        flash("Nemáte oprávnění k této stránce.", "danger")
        return redirect(url_for("main.homepage"))

    pacienti = (
        db.session.query(User)
        .join(PacientLekar, PacientLekar.pacient_id == User.id)
        .filter(PacientLekar.lekar_id == current_user.id, PacientLekar.stav == 1)
        .all()
    )

    return render_template("moji_pacienti.html", pacienti=pacienti)