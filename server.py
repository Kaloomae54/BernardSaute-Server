from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

USERS_FILE = "users.json"

if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({}, f)

def load_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

@app.route("/")
def home():
    return "Bernard Saute API fonctionne"

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    users = load_users()
    if username in users:
        return jsonify({"error": "User already exists"}), 400

    users[username] = {
        "password": password,
        "points": 0,
        "current_skin": "bernard_classic",
        "shop_items": {
            "bernard_classic": True
        }
    }
    save_users(users)
    return jsonify(users[username]), 200

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    users = load_users()
    if username not in users or users[username]["password"] != password:
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify(users[username]), 200

@app.route("/update", methods=["POST"])
def update_user():
    data = request.get_json()
    username = data.get("username")
    user_data = data.get("data")

    users = load_users()
    if username in users:
        users[username] = user_data
        save_users(users)
        return jsonify({"success": True}), 200

    return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
