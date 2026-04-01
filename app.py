from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pickle
import os

app = Flask(__name__)

# 🔥 Libera qualquer origem (CORS)
CORS(app, resources={r"/*": {"origins": "*"}})

# 🔥 Carregar modelo
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# 🔥 Serve o frontend (index.html)
@app.route("/")
def home():
    return send_from_directory(".", "index.html")

# 🔥 Rota de previsão
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        if not data or "url" not in data:
            return jsonify({"erro": "URL não fornecida"}), 400

        url = data["url"]

        vector = vectorizer.transform([url])
        prediction = model.predict(vector)[0]

        result = "Phishing" if prediction == 1 else "Seguro"

        return jsonify({"resultado": result})

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# 🔥 CONFIGURAÇÃO PARA RAILWAY (ESSENCIAL)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)