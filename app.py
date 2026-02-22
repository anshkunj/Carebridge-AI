from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def calculate_risk(symptoms, age):
    score = 0

    symptoms = symptoms.lower()

    if "fever" in symptoms:
        score += 1
    if "cough" in symptoms:
        score += 1
    if "shortness of breath" in symptoms:
        score += 3
    if "chest pain" in symptoms:
        score += 4
    if "dizziness" in symptoms:
        score += 2

    if age >= 60:
        score += 2

    if score <= 2:
        return "Low"
    elif score <= 5:
        return "Moderate"
    else:
        return "High"

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    symptoms = data.get("symptoms", "")
    age = int(data.get("age", 0))

    risk = calculate_risk(symptoms, age)

    return jsonify({"risk": risk})

if __name__ == "__main__":
    app.run(host="0.0.0.0")
