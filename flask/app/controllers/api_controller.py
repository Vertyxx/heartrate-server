from flask import Blueprint, request, jsonify
from app import db
from app.models.user_model import SrdecniAktivita
from datetime import datetime

api = Blueprint("api", __name__)

@api.route("/heart_rate", methods=["POST"])
def record_heart_rate():
    """Přijme JSON s tepovou frekvencí a časem a uloží do DB."""
    try:
        data = request.get_json()

        if not data or "pacient_id" not in data or "bpm" not in data or "cas" not in data or "cviceni" not in data:
            return jsonify({"error": "Invalid input"}), 400

        pacient_id = int(data["pacient_id"])
        bpm = float(data["bpm"])
        cas = datetime.strptime(data["cas"], "%Y-%m-%d %H:%M:%S")  # Očekává formát: "2025-03-12 14:30:00"
        cviceni = int(data["cviceni"])

        new_entry = SrdecniAktivita(pacient_id=pacient_id, bpm=bpm, cas=cas, cviceni=cviceni)
        db.session.add(new_entry)
        db.session.commit()

        return jsonify({"message": "Heart rate recorded"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500