from flask import Flask, request, jsonify
import json
import os
import hashlib

app = Flask(__name__)

DATA_FILE = "users_data.json"

# Chargement des données utilisateurs
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        users_db = json.load(f)
else:
    users_db = {}

def save_db():
    with open(DATA_FILE, "w") as f:
        json.dump(users_db, f, indent=4)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Nom d'utilisateur et mot de passe requis"}), 400

    if username in users_db:
        return jsonify({"error": "Nom d'utilisateur déjà pris"}), 400

    users_db[username] = {
        "password": hash_password(password),
        "points": 0,
        "shop_items": {"Bernard": True},
        "current_skin": "Bernard"
    }
    save_db()
    return jsonify({"message": "Inscription réussie", "points": 0, "shop_items": {"Bernard": True}, "current_skin": "Bernard"}), 200

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Nom d'utilisateur et mot de passe requis"}), 400

    user = users_db.get(username)
    if not user or user["password"] != hash_password(password):
        return jsonify({"error": "Identifiants invalides"}), 401

    # On renvoie les données nécessaires au client
    return jsonify({
        "message": "Connexion réussie",
        "points": user.get("points", 0),
        "shop_items": user.get("shop_items", {"Bernard": True}),
        "current_skin": user.get("current_skin", "Bernard")
    }), 200

@app.route('/update', methods=['POST'])
def update():
    data = request.get_json()
    username = data.get("username")
    new_data = data.get("data")

    if not username or not new_data:
        return jsonify({"error": "Données manquantes"}), 400

    if username not in users_db:
        return jsonify({"error": "Utilisateur non trouvé"}), 404

    # Mise à jour simple (à adapter selon les besoins)
    users_db[username].update(new_data)
    save_db()

    return jsonify({"message": "Données mises à jour"}), 200

@app.route("/leaderboard", methods=["GET"])
def leaderboard():
    top = sorted(users_db.items(), key=lambda x: x[1].get("points", 0), reverse=True)
    result = [{"username": u, "points": d.get("points", 0)} for u, d in top[:10]]
    return jsonify(result), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
