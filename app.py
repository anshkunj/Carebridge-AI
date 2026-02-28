from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import io
import os

app = Flask(__name__)

# Allow frontend access
CORS(app, resources={r"/*": {"origins": "*"}})


# -----------------------------
# HEALTH ANALYSIS ENGINE
# -----------------------------

def analyze_health(symptoms, age):

    symptoms = symptoms.lower()

    score = 0
    explanation_list = []

    # Symptom weights
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

    # Detect symptoms safely
    for symptom, weight in symptom_weights.items():
        if symptom in symptoms:
            score += weight
            explanation_list.append(f"{symptom.title()} detected")

    # Age risk factors
    if age >= 60:
        score += 4
        explanation_list.append("Senior age risk factor")

    if age <= 5 and age > 0:
        score += 3
        explanation_list.append("Child age risk factor")

    # -----------------------------
    # Emergency Overrides
    # -----------------------------

    # More strict detection
    symptom_tokens = [s.strip() for s in symptoms.split(",")]

    if "chest pain" in symptom_tokens or "emergency" in symptom_tokens:
        return {
            "risk": "EMERGENCY",
            "confidence": 95,
            "explanation": "Seek emergency medical help immediately",
            "hospital_map": "https://www.google.com/maps/search/?api=1&query=hospital+near+me"
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

    # Confidence calculation
    confidence = min(98, 65 + (score * 2.5))

    explanation_text = " | ".join(explanation_list)
    if explanation_text:
        explanation_text += ". "

    explanation_text += advice

    return {
        "risk": risk,
        "confidence": round(confidence, 2),
        "explanation": explanation_text,
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


# -----------------------------
# Risk Analysis Endpoint
# -----------------------------

@app.route("/analyze", methods=["POST"])
def analyze():

    try:
        data = request.json or {}

        symptoms = data.get("symptoms", "")
        age = int(data.get("age", 0))

        result = analyze_health(symptoms, age)

        return jsonify(result)

    except Exception:
        return jsonify({
            "risk": "Error",
            "confidence": 0,
            "explanation": "Server processing error"
        }), 500


# -----------------------------
# REPORT GENERATION
# -----------------------------

@app.route("/generate-report", methods=["POST"])
def generate_report():

    try:
        data = request.json or {}

        symptoms = data.get("symptoms", "")
        age = int(data.get("age", 0))

        result = analyze_health(symptoms, age)

        buffer = io.BytesIO()

        doc = SimpleDocTemplate(buffer)

        styles = getSampleStyleSheet()

        report_text = f"""
CareBridge Health Report

Age: {age}
Symptoms: {symptoms}

Risk Level: {result['risk']}
Confidence: {result['confidence']}%

Advice:
{result['explanation']}
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

    except Exception:
        return jsonify({"error": "Report generation failed"}), 500


# -----------------------------

if __name__ == "__main__":
    import os
    
    port = int(os.environ.get("PORT", 10000))

    app.run(
        host="0.0.0.0",
        port=port
    )