from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Serveur Bernard Saute en ligne 🚀"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render fournit automatiquement la variable PORT
    app.run(host="0.0.0.0", port=port)        # Très important pour que Render détecte le port
