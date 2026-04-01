print("Training Started...")

import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import pickle

# Load Kaggle SMS Spam dataset
df = pd.read_csv("spam.csv", encoding="latin-1")

# Keep only required columns
df = df[['v1', 'v2']]
df.columns = ['label', 'text']

print("Dataset Loaded Successfully")
print(df.head())

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Text preprocessing function
def preprocess(text):
    doc = nlp(text.lower())
    tokens = [
        token.lemma_
        for token in doc
        if not token.is_stop and not token.is_punct
    ]
    return " ".join(tokens)

# Clean text
df["clean_text"] = df["text"].apply(preprocess)

# Convert text to numeric features
vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(df["clean_text"])
y = df["label"]

# Train/Test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)

print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n")
print(classification_report(y_test, y_pred))

# Save model
pickle.dump(model, open("spam_model.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))

print("\nModel saved successfully!")