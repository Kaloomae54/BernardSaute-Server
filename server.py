from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import hashlib

app = Flask(__name__)
CORS(app)

USERS_FILE = "users.json"

# Chargement des utilisateurs
if os.path.exists(USERS_FILE):
    with open(USERS_FILE, "r") as f:
        users = json.load(f)
else:
    users = {}

def save_users():
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    if username in users:
        return jsonify({"error": "Utilisateur déjà existant"}), 400

    users[username] = {
        "password": hash_password(password),
        "points": 0,
        "current_skin": "bernard_classic",
        "shop_items": {"bernard_classic": True}
    }
    save_users()
    user_data = users[username].copy()
    user_data.pop("password")
    return jsonify(user_data)

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    user = users.get(username)
    if user and user["password"] == hash_password(password):
        user_data = user.copy()
        user_data.pop("password")
        return jsonify(user_data)
    return jsonify({"error": "Identifiants invalides"}), 401

@app.route("/update", methods=["POST"])
def update_user():
    data = request.json
    username = data.get("username")
    user_data = data.get("data")
    if username in users:
        # Ne pas écraser le mot de passe
        password = users[username]["password"]
        users[username] = user_data
        users[username]["password"] = password
        save_users()
        return jsonify(success=True)
    return jsonify({"error": "Utilisateur introuvable"}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
