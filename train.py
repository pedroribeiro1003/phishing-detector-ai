import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

# Dataset simples (vamos usar manual primeiro)
data = {
    "url": [
        "https://google.com",
        "https://facebook.com",
        "http://fake-bank-login.com",
        "http://verify-account-now.com",
        "https://github.com",
        "http://secure-login-paypal.com"
    ],
    "label": [0, 0, 1, 1, 0, 1]
}

df = pd.DataFrame(data)

# IA
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df['url'])
y = df['label']

model = LogisticRegression()
model.fit(X, y)

# Salvar modelo
pickle.dump(model, open("model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("Modelo treinado!")