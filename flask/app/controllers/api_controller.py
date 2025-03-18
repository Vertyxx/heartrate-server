from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user_model import SrdecniAktivita
from datetime import datetime

api = Blueprint("api", __name__)

@api.route("/heart_rate", methods=["POST"])
@jwt_required()  # 🛠 API endpoint je nyní chráněný JWT
def record_heart_rate():
    """Přijme JSON s jedním nebo více záznamy tepové frekvence a uloží je do DB."""
    try:
        user_id = get_jwt_identity()  # 🛠 Získání ID přihlášeného uživatele z JWT tokenu
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid input"}), 400

        # Zajistíme, že data je seznam, i když přijde jen jeden záznam
        if not isinstance(data, list):
            data = [data]

        new_entries = []
        for item in data:
            if not all(key in item for key in ("bpm", "cas", "cviceni")):
                return jsonify({"error": "Invalid input in one of the records"}), 400

            new_entries.append(SrdecniAktivita(
                uzivatel_id=user_id,  # 🛠 Použití ID uživatele z JWT tokenu
                bpm=float(item["bpm"]),
                cas=datetime.strptime(item["cas"], "%Y-%m-%d %H:%M:%S"),
                cviceni=int(item["cviceni"])
            ))

        # Přidání všech záznamů najednou
        db.session.add_all(new_entries)
        db.session.commit()

        return jsonify({"message": f"{len(new_entries)} heart rate record(s) recorded"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500