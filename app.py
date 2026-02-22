from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

# Symptom weights
SYMPTOM_WEIGHTS = {
    "fever": 2,
    "cough": 2,
    "headache": 1,
    "fatigue": 1,
    "dizziness": 2,
    "vomiting": 3,
    "chest pain": 5,
    "shortness of breath": 5,
    "breathing difficulty": 5,
    "unconscious": 6
}

SEVERE_WORDS = ["severe", "extreme", "intense", "very bad", "unbearable"]

def calculate_ai_risk(symptoms, age):
    text = symptoms.lower()
    score = 0
    detected = []

    # Detect symptoms
    for symptom, weight in SYMPTOM_WEIGHTS.items():
        if symptom in text:
            score += weight
            detected.append(symptom)

    # Detect severity words
    for word in SEVERE_WORDS:
        if word in text:
            score += 2

    # Age factor
    if age >= 60:
        score += 3
    elif age <= 5:
        score += 2

    # Multi-symptom boost
    if len(detected) >= 3:
        score += 2

    # Risk classification
    if score <= 3:
        risk = "Low"
    elif score <= 8:
        risk = "Moderate"
    else:
        risk = "High"

    explanation = generate_explanation(risk, detected, age)

    return risk, explanation


def generate_explanation(risk, detected, age):
    if risk == "Low":
        return f"Symptoms detected: {', '.join(detected)}. Currently appears mild. Monitor condition and rest."

    elif risk == "Moderate":
        return f"Multiple symptoms detected ({', '.join(detected)}). Consider consulting a healthcare provider if condition worsens."

    else:
        return f"Serious symptoms detected ({', '.join(detected)}). Immediate medical attention is recommended."


@app.route("/")
def home():
    return "CareBridge AI Engine Running 🚀"

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    symptoms = data.get("symptoms", "")
    age = int(data.get("age", 0))

    risk, explanation = calculate_ai_risk(symptoms, age)

    return jsonify({
        "risk": risk,
        "explanation": explanation
    })


if __name__ == "__main__":
    app.run()