from flask import Blueprint, request, jsonify
from app import db
from app.models.user_model import SrdecniAktivita
from datetime import datetime

api = Blueprint("api", __name__)

@api.route("/heart_rate", methods=["POST"])
def record_heart_rate():
    """Přijme JSON s jedním nebo více záznamy tepové frekvence a uloží je do DB."""
    try:
        data = request.get_json()

        # Ověření, zda data nejsou prázdná
        if not data:
            return jsonify({"error": "Invalid input"}), 400

        # Pokud je data seznam, zpracujeme více položek, jinak jen jednu
        if isinstance(data, list):
            new_entries = []
            for item in data:
                if "pacient_id" not in item or "bpm" not in item or "cas" not in item or "cviceni" not in item:
                    return jsonify({"error": "Invalid input in one of the records"}), 400
                
                new_entries.append(SrdecniAktivita(
                    pacient_id=int(item["pacient_id"]),
                    bpm=float(item["bpm"]),
                    cas=datetime.strptime(item["cas"], "%Y-%m-%d %H:%M:%S"),
                    cviceni=int(item["cviceni"])
                ))

            # Přidání všech záznamů najednou
            db.session.add_all(new_entries)
            db.session.commit()

            return jsonify({"message": f"{len(new_entries)} heart rate records recorded"}), 201
        
        else:
            # Pokud přijde pouze jeden objekt, zpracujeme ho normálně
            if "pacient_id" not in data or "bpm" not in data or "cas" not in data or "cviceni" not in data:
                return jsonify({"error": "Invalid input"}), 400

            new_entry = SrdecniAktivita(
                pacient_id=int(data["pacient_id"]),
                bpm=float(data["bpm"]),
                cas=datetime.strptime(data["cas"], "%Y-%m-%d %H:%M:%S"),
                cviceni=int(data["cviceni"])
            )
            db.session.add(new_entry)
            db.session.commit()

            return jsonify({"message": "Heart rate recorded"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500