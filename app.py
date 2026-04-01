from flask import Flask, request, jsonify
import pickle

# create flask app
app = Flask(__name__)

# load model
model = pickle.load(open("spam_model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

@app.route("/")
def home():
    return "Spam Detection API Running"

# Only POST, since Apps Script sends JSON
@app.route("/check", methods=["POST"])
def check_spam():

    data = request.get_json()  # <-- read JSON payload
    email_text = data.get("email_text", "")
    keyword = data.get("keyword", "")  # optional

    # convert text
    text_vector = vectorizer.transform([email_text])

    # predict
    spam_prob = model.predict_proba(text_vector)[0][1]

    final_score = spam_prob

    # apply keyword bypass if present
    if keyword and keyword.lower() in email_text.lower():
        final_score -= 0.20

    prediction = "spam" if final_score > 0.5 else "ham"

    return jsonify({
        "spam_probability": float(spam_prob),
        "final_score": float(final_score),
        "prediction": prediction
    })


if __name__ == "__main__":
    app.run(debug=True)