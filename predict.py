import pickle
import spacy

print("Loading Advanced Spam Engine...")

# Load model & vectorizer
model = pickle.load(open("spam_model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# Load spaCy for NER
nlp = spacy.load("en_core_web_sm")

# User safe keyword
safe_keyword = input("Enter your SAFE keyword: ").lower()

def preprocess(text):
    doc = nlp(text.lower())
    tokens = [
        token.lemma_
        for token in doc
        if not token.is_stop and not token.is_punct
    ]
    return " ".join(tokens)

while True:
    email = input("\nEnter email text (type 'exit' to quit): ")

    if email.lower() == "exit":
        break

    clean_email = preprocess(email)
    vectorized_email = vectorizer.transform([clean_email])

    # Get spam probability
    prob = model.predict_proba(vectorized_email)[0]
    spam_probability = prob[list(model.classes_).index("spam")]

    final_score = spam_probability

    # 🔑 Keyword Trust Boost
    if safe_keyword in email.lower() and spam_probability < 0.30:
        print("Keyword detected → Trust Boost Applied (-0.20)")
        final_score -= 0.20
    elif safe_keyword in email.lower():
        print("Keyword detected but spam probability high → No boost applied")

    # 🧠 NER Trust Detection
    doc = nlp(email)
    trusted_entities = [ent.text for ent in doc.ents if ent.label_ in ["ORG", "PERSON"]]

    if trusted_entities:
        print("Trusted Entity Detected:", trusted_entities)
        print("Entity Trust Boost Applied (-0.15)")
        final_score -= 0.15

    print(f"Spam Probability: {spam_probability:.2f}")
    print(f"Final Adjusted Score: {final_score:.2f}")

    if final_score > 0.30:
        print("Final Prediction: SPAM ❌")
    else:
        print("Final Prediction: HAM ✅")