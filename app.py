from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle

app = Flask(__name__)

# 🔥 Libera qualquer origem (resolve CORS de vez)
CORS(app, resources={r"/*": {"origins": "*"}})

model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

@app.route("/")
def home():
    return "API de Phishing rodando 🚀"

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


if __name__ == "__main__":
    app.run(debug=True)