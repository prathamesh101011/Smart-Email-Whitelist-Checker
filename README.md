# AI Spam Gmail Add-on

## Description
This project detects spam emails using Machine Learning and integrates with Gmail using a custom Add-on.

## Features
- Spam detection using ML (TF-IDF + model)
- Keyword whitelist system
- Gmail Add-on integration
- Flask API backend

## How to Run

```bash
pip install -r requirements.txt
python app.py
ngrok http 5000

## Project Structure

- app.py → Flask API (backend server)
- predict.py → CLI testing script
- train_model.py → Model training code
- spam_model.pkl → Trained ML model
- vectorizer.pkl → TF-IDF vectorizer
- apps_script/ → Gmail Add-on code