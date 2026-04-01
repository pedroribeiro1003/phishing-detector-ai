from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pickle
import os

app = Flask(__name__)

# 🔥 Libera qualquer origem (CORS)
CORS(app, resources={r"/*": {"origins": "*"}})

# 🔥 Caminho absoluto (IMPORTANTE no Railway)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model_path = os.path.join(BASE_DIR, "model.pkl")
vectorizer_path = os.path.join(BASE_DIR, "vectorizer.pkl")

# 🔥 Carregar modelo com segurança
try:
    model = pickle.load(open(model_path, "rb"))
    vectorizer = pickle.load(open(vectorizer_path, "rb"))
    print("✅ Modelo carregado com sucesso")
except Exception as e:
    print("❌ ERRO ao carregar modelo:", e)
    model = None
    vectorizer = None


# 🔥 Serve o frontend (index.html)
@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")


# 🔥 Rota de previsão
@app.route("/predict", methods=["POST"])
def predict():
    try:
        if model is None or vectorizer is None:
            return jsonify({"erro": "Modelo não carregado"}), 500

        data = request.get_json()

        if not data or "url" not in data:
            return jsonify({"erro": "URL não fornecida"}), 400

        url = data["url"]

        vector = vectorizer.transform([url])
        prediction = model.predict(vector)[0]

        result = "Phishing" if prediction == 1 else "Seguro"

        return jsonify({"resultado": result})

    except Exception as e:
        print("❌ ERRO NO PREDICT:", e)
        return jsonify({"erro": str(e)}), 500


# 🔥 CONFIGURAÇÃO PARA RAILWAY (ESSENCIAL)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)