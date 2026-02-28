from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# -----------------------------
# HEALTH ANALYSIS ENGINE
# -----------------------------

def analyze_health(symptoms, age):

    symptoms = symptoms.lower()

    score = 0
    explanation_list = []

    # Symptom scoring
    if "fever" in symptoms:
        score += 2
        explanation_list.append("Fever detected")

    if "cough" in symptoms:
        score += 2
        explanation_list.append("Cough symptoms present")

    if "breathing" in symptoms or "shortness" in symptoms:
        score += 5
        explanation_list.append("Breathing difficulty detected")

    if "chest pain" in symptoms:
        score += 6
        explanation_list.append("Chest pain is a serious symptom")

    if "headache" in symptoms:
        score += 1

    # Age risk factors
    if age >= 60:
        score += 3
        explanation_list.append("Senior age risk factor")

    if age <= 5:
        score += 2

    # -----------------------------
    # RISK CLASSIFICATION
    # -----------------------------

    if "chest pain" in symptoms or "emergency" in symptoms:
        risk = "EMERGENCY"
        advice = "Seek emergency medical help immediately"

        hospital_link = "https://www.google.com/maps/search/hospital+near+me"

    elif score <= 3:
        risk = "Low"
        advice = "Rest, hydrate well, monitor symptoms"

        hospital_link = "https://www.google.com/search?q=home+care+tips"

    elif score <= 7:
        risk = "Moderate"
        advice = "Consider consulting a doctor if symptoms persist"

        hospital_link = "https://www.google.com/maps/search/clinic+near+me"

    else:
        risk = "High"
        advice = "Medical consultation recommended as soon as possible"

        hospital_link = "https://www.google.com/maps/search/hospital+near+me"

    # -----------------------------
    # Sustainability Score (Hackathon bonus 😼)
    # -----------------------------

    sustainability_score = max(100 - (score * 10), 30)

    return {
        "risk": risk,
        "confidence": min(95, 70 + score * 3),
        "explanation": " | ".join(explanation_list) + ". " + advice,
        "sustainability": sustainability_score,
        "hospital_map": hospital_link
    }


# -----------------------------
# ROUTES
# -----------------------------

@app.route("/")
def home():
    return """
    <html>
    <head>
    <title>CareBridge AI</title>
    </head>

    <body style="background:#0f172a;color:white;
    height:100vh;display:flex;
    justify-content:center;
    align-items:center;
    font-family:sans-serif">

    <div style="text-align:center">
        <h1>🚑 CareBridge AI</h1>
        <p>Accessibility First Health Risk Analyzer</p>

        <a href="https://anshkunj.github.io/Carebridge-AI"
        style="padding:14px 28px;
        background:#38bdf8;
        color:black;
        text-decoration:none;
        border-radius:12px;
        font-weight:bold;
        display:inline-block;
        margin-top:20px">

        Open CareBridge Frontend 🌍

        </a>
    </div>

    </body>
    </html>
    """


@app.route("/analyze", methods=["POST"])
def analyze():

    try:
        data = request.json

        symptoms = data.get("symptoms", "")
        age = int(data.get("age", 0))

        result = analyze_health(symptoms, age)

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "risk": "Error",
            "confidence": 0,
            "explanation": "Invalid input data",
            "error": str(e)
        }), 400


# -----------------------------

if __name__ == "__main__":
    app.run()