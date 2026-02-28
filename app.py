from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import io

app = Flask(__name__)
CORS(app)

# -----------------------------
# HEALTH ANALYSIS ENGINE
# -----------------------------

def analyze_health(symptoms, age):

    symptoms = symptoms.lower()

    score = 0
    explanation_list = []

    # -----------------------------
    # Symptom Risk Weighting
    # -----------------------------

    symptom_weights = {
        "fever": 2,
        "cough": 2,
        "breathing": 5,
        "shortness": 5,
        "chest pain": 8,
        "headache": 1,
        "dizziness": 2,
        "vomiting": 3,
        "fatigue": 1
    }

    for symptom, weight in symptom_weights.items():
        if symptom in symptoms:
            score += weight
            explanation_list.append(f"{symptom.title()} detected")

    # -----------------------------
    # Age Risk Factors
    # -----------------------------

    if age >= 60:
        score += 4
        explanation_list.append("Senior age risk factor")

    if age <= 5:
        score += 3
        explanation_list.append("Child age risk factor")

    # -----------------------------
    # Emergency Overrides (VERY IMPORTANT ⚠️)
    # -----------------------------

    if "chest pain" in symptoms or "emergency" in symptoms:
        risk = "EMERGENCY"
        advice = "Seek emergency medical help immediately"
        hospital_link = "https://www.google.com/maps/search/?api=1&query=hospital+near+me"

        return {
            "risk": risk,
            "confidence": 95,
            "explanation": advice,
            "hospital_map": hospital_link
        }

    # -----------------------------
    # Risk Classification
    # -----------------------------

    if score <= 4:
        risk = "Low"
        advice = "Rest, hydrate and monitor symptoms"
        hospital_link = "https://www.google.com/search?q=home+care+tips"

    elif score <= 10:
        risk = "Moderate"
        advice = "Consult doctor if symptoms persist"
        hospital_link = "https://www.google.com/maps/search/?api=1&query=clinic+near+me"

    else:
        risk = "High"
        advice = "Medical consultation strongly recommended"
        hospital_link = "https://www.google.com/maps/search/?api=1&query=hospital+near+me"

    # -----------------------------
    # Confidence Calculation
    # -----------------------------

    confidence = min(98, 65 + (score * 2.5))

    return {
        "risk": risk,
        "confidence": round(confidence, 2),
        "explanation": " | ".join(explanation_list) + ". " + advice,
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

    <body style="
    background:#0f172a;
    color:white;
    height:100vh;
    display:flex;
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
        Open Frontend 🌍
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
            "explanation": str(e)
        }), 400


# -----------------------------
# REPORT GENERATION (BEST METHOD ⭐)
# -----------------------------

@app.route("/generate-report", methods=["POST"])
def generate_report():

    data = request.json

    symptoms = data.get("symptoms", "")
    age = int(data.get("age", 0))

    result = analyze_health(symptoms, age)

    # Generate PDF in memory (VERY IMPORTANT)
    buffer = io.BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    report_text = f"""
<b>CareBridge Health Report</b><br/><br/>
Age: {age}<br/>
Symptoms: {symptoms}<br/>
Risk Level: {result['risk']}<br/>
Confidence: {result['confidence']}%<br/><br/>
Advice: {result['explanation']}
"""

    story = [Paragraph(report_text, styles["Normal"])]

    doc.build(story)

    buffer.seek(0)

    return send_file(
        buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="CareBridge_Report.pdf"
    )


# -----------------------------

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )
