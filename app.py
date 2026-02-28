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
        explanation_list.append("Chest pain is serious symptom")

    if "headache" in symptoms:
        score += 1

    if age >= 60:
        score += 3
        explanation_list.append("Senior age risk factor")

    if age <= 5:
        score += 2

    # Risk classification
    if "chest pain" in symptoms or "emergency" in symptoms:
        risk = "EMERGENCY"
        advice = "Seek emergency medical help immediately"
        hospital_link = "https://www.google.com/maps/search/hospital+near+me"

    elif score <= 3:
        risk = "Low"
        advice = "Rest, hydrate and monitor symptoms"
        hospital_link = "https://www.google.com/search?q=home+care+tips"

    elif score <= 7:
        risk = "Moderate"
        advice = "Consider consulting doctor if symptoms persist"
        hospital_link = "https://www.google.com/maps/search/clinic+near+me"

    else:
        risk = "High"
        advice = "Medical consultation recommended urgently"
        hospital_link = "https://www.google.com/maps/search/hospital+near+me"

    return {
        "risk": risk,
        "confidence": min(95, 70 + score * 3),
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
    CareBridge Health Report

    Age: {age}

    Symptoms: {symptoms}

    Risk Level: {result['risk']}

    Confidence: {result['confidence']}%

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