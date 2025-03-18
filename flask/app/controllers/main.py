from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user        # type: ignore
from app import db
from app.models.user_model import SrdecniAktivita, User, PacientLekar

main = Blueprint('main', __name__)

#!!!Dodelat logiku pro neprihlaseneho uzivtaele!!!!
@main.route("/")
def homepage():
    # Pokud není přihlášený uživatel, vrátí se stránka bez pokusu o načítání dat
    if not current_user.is_authenticated:
        return render_template("homepage.html", message="Prosím přihlaste se pro zobrazení srdeční aktivity.")

    # Získání srdeční aktivity pro aktuálního uživatele (pacienta i lékaře)
    aktivity = (
        db.session.query(SrdecniAktivita.cas, SrdecniAktivita.bpm, SrdecniAktivita.cviceni)
        .filter(SrdecniAktivita.uzivatel_id == current_user.id)
        .order_by(SrdecniAktivita.cas.asc())
        .all()
    )

    # Převod dat na seznamy pro JSON
    casove_razitka = [a.cas.strftime("%Y-%m-%d %H:%M:%S") for a in aktivity] if aktivity else []
    hodnoty_srdce = [a.bpm for a in aktivity] if aktivity else []
    cviceni_hodnoty = [a.cviceni for a in aktivity] if aktivity else []

    return render_template(
        "homepage.html",
        casove_razitka=casove_razitka,
        hodnoty_srdce=hodnoty_srdce,
        cviceni_hodnoty=cviceni_hodnoty
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
    zadosti_lekar = (
        db.session.query(User.id, User.jmeno, User.prijmeni)
        .join(PacientLekar, PacientLekar.pacient_id == User.id)
        .filter(PacientLekar.lekar_id == current_user.id, PacientLekar.stav == 4)
        .all()
    )

    return render_template("moji_pacienti.html", pacienti=pacienti, zadosti_lekar=zadosti_lekar)

@main.route("/pacient/<int:pacient_id>")
@login_required
def pacient_detail(pacient_id):
    pacient = db.session.get(User, pacient_id)

    if not pacient or pacient.role != "pacient":
        flash("Pacient nenalezen.", "danger")
        return redirect(url_for("main.moji_pacienti"))

    aktivity = (
        db.session.query(SrdecniAktivita.cas, SrdecniAktivita.bpm, SrdecniAktivita.cviceni)
        .filter(SrdecniAktivita.uzivatel_id == pacient_id)
        .order_by(SrdecniAktivita.cas.asc())
        .all()
    )

    casove_razitka = [a.cas.strftime("%Y-%m-%d %H:%M:%S") for a in aktivity] if aktivity else []
    hodnoty_srdce = [a.bpm for a in aktivity] if aktivity else []
    cviceni_hodnoty = [a.cviceni for a in aktivity] if aktivity else []

    return render_template(
        "pacient_detail.html",
        pacient=pacient,
        casove_razitka=casove_razitka,
        hodnoty_srdce=hodnoty_srdce,
        cviceni_hodnoty=cviceni_hodnoty
    )

@main.route("/schvalit-zadost-lekar", methods=["POST"])  # Lékař schvaluje žádost pacienta
@login_required
def schvalit_zadost_lekar():
    if current_user.role != "lekar":
        flash("Nemáte oprávnění k této akci.", "danger")
        return redirect(url_for("main.moji_pacienti"))

    pacient_id = request.form.get("pacient_id")

    zadost = db.session.query(PacientLekar).filter_by(pacient_id=pacient_id, lekar_id=current_user.id, stav=4).first()
    if zadost:
        zadost.stav = 1  # Schváleno
        db.session.commit()
        flash("Žádost pacienta byla schválena.", "success")

    return redirect(url_for("main.moji_pacienti"))


@main.route("/odmitnout-zadost-lekar", methods=["POST"])  # Lékař odmítá žádost pacienta
@login_required
def odmitnout_zadost_lekar():
    if current_user.role != "lekar":
        flash("Nemáte oprávnění k této akci.", "danger")
        return redirect(url_for("main.moji_pacienti"))

    pacient_id = request.form.get("pacient_id")

    zadost = db.session.query(PacientLekar).filter_by(pacient_id=pacient_id, lekar_id=current_user.id, stav=4).first()
    if zadost:
        zadost.stav = 0  # Odmítnuto
        db.session.commit()
        flash("Žádost pacienta byla odmítnuta.", "warning")

    return redirect(url_for("main.moji_pacienti"))


@main.route("/moji-lekari")
@login_required
def moji_lekari():
    if current_user.role != "pacient":
        flash("Nemáte oprávnění k této stránce.", "danger")
        return redirect(url_for("main.homepage"))

    # Seznam lékařů pacienta (stav = 1 → schváleno)
    lekari = (
        db.session.query(User)
        .join(PacientLekar, PacientLekar.lekar_id == User.id)
        .filter(PacientLekar.pacient_id == current_user.id, PacientLekar.stav == 1)
        .all()
    )

    # Žádosti od lékařů k potvrzení (stav = 3 → lékař poslal žádost pacientovi)
    zadosti_pacient = (
        db.session.query(User.id, User.jmeno, User.prijmeni, User.zamereni)
        .join(PacientLekar, PacientLekar.lekar_id == User.id)
        .filter(PacientLekar.pacient_id == current_user.id, PacientLekar.stav == 3)
        .all()
    )

    return render_template("moji_lekari.html", lekari=lekari, zadosti_pacient=zadosti_pacient)

@main.route("/schvalit-zadost-pacient", methods=["POST"])  # Pacient schvaluje žádost lékaře
@login_required
def schvalit_zadost_pacient():
    if current_user.role != "pacient":
        flash("Nemáte oprávnění k této akci.", "danger")
        return redirect(url_for("main.moji_lekari"))

    lekar_id = request.form.get("lekar_id")

    zadost = db.session.query(PacientLekar).filter_by(
        pacient_id=current_user.id, lekar_id=lekar_id, stav=3
    ).first()

    if zadost:
        zadost.stav = 1  # Schváleno
        db.session.commit()
        flash("Žádost lékaře byla schválena.", "success")

    return redirect(url_for("main.moji_lekari"))


@main.route("/odmitnout-zadost-pacient", methods=["POST"])  # Pacient odmítá žádost lékaře
@login_required
def odmitnout_zadost_pacient():
    if current_user.role != "pacient":
        flash("Nemáte oprávnění k této akci.", "danger")
        return redirect(url_for("main.moji_lekari"))

    lekar_id = request.form.get("lekar_id")

    zadost = db.session.query(PacientLekar).filter_by(
        pacient_id=current_user.id, lekar_id=lekar_id, stav=3
    ).first()

    if zadost:
        zadost.stav = 0  # Odmítnuto
        db.session.commit()
        flash("Žádost lékaře byla odmítnuta.", "warning")

    return redirect(url_for("main.moji_lekari"))