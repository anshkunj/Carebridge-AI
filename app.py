from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from config import Config
from utils import (
    analyze_health,
    calculate_green_score,
    estimate_environmental_impact,
    generate_medical_summary
)

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER

import logging
import io
import os

# --------------------------------
# App Initialization
# --------------------------------

app = Flask(__name__)
app.config.from_object(Config)

CORS(app, resources={r"/*": {"origins": app.config["ALLOWED_ORIGINS"]}})
logging.basicConfig(level=logging.INFO)

# --------------------------------
# HOME ROUTE
# --------------------------------

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

# --------------------------------
# ANALYZE ENDPOINT
# --------------------------------

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.json or {}

        symptoms = data.get("symptoms", "")
        age = int(data.get("age", 0))
        location = data.get("location", "")

        # Health Analysis
        health_result = analyze_health(symptoms, age)

        # Sustainability Analysis (corrected)
        green_score = calculate_green_score(health_result["risk"])
        environmental_impact = estimate_environmental_impact(health_result["risk"])

        return jsonify({
            "risk": health_result["risk"],
            "confidence": health_result["confidence"],
            "explanation": health_result["explanation"],
            "hospital_map": health_result.get("hospital_map", ""),
            "green_score": green_score,
            "environmental_impact": environmental_impact,
            "disclaimer": app.config["MEDICAL_DISCLAIMER"]
        })

    except Exception as e:
        logging.error(f"Analyze Error: {str(e)}")
        return jsonify({"error": "Server processing error"}), 500


# --------------------------------
# REPORT GENERATION
# --------------------------------

@app.route("/generate-report", methods=["POST"])
def generate_report():
    try:
        data = request.json or {}

        symptoms = data.get("symptoms", "")
        age = int(data.get("age", 0))

        # Health Analysis
        health_result = analyze_health(symptoms, age)

        # Sustainability Analysis (corrected)
        green_score = calculate_green_score(health_result["risk"])
        environmental_impact = estimate_environmental_impact(health_result["risk"])

        summary = generate_medical_summary(health_result)

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer)

        elements = []

        # Styles
        title_style = ParagraphStyle(
            name="title",
            fontSize=22,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#0ea5e9"),
            spaceAfter=20
        )

        normal_style = ParagraphStyle(
            name="normal",
            fontSize=11,
            leading=18
        )

        # Title
        elements.append(
            Paragraph("🚑 CareBridge AI Integrated Healthcare Report", title_style)
        )
        elements.append(Spacer(1, 20))

        # Table Data
        table_data = [
            ["Field", "Value"],
            ["Age", str(age)],
            ["Symptoms", symptoms],
            ["Risk Level", health_result["risk"]],
            ["Confidence", str(health_result["confidence"]) + "%"],
            ["Green Score", str(green_score)],
            ["CO2 Saved (kg)", str(environmental_impact.get("co2_saved", 0))],
            ["Paper Saved (pages)", str(environmental_impact.get("paper_saved", 0))]
        ]

        table = Table(table_data, colWidths=[180, 320])

        table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#0ea5e9")),
            ("TEXTCOLOR", (0,0), (-1,0), colors.white),
            ("GRID", (0,0), (-1,-1), 1, colors.HexColor("#38bdf8")),
            ("PADDING", (0,0), (-1,-1), 8),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 25))

        # Medical Summary
        elements.append(Paragraph("🧠 Medical Insight", title_style))
        elements.append(Spacer(1, 10))
        elements.append(Paragraph(summary, normal_style))
        elements.append(Spacer(1, 20))

        # Disclaimer
        elements.append(Paragraph("⚠ Disclaimer", title_style))
        elements.append(Spacer(1, 10))
        elements.append(Paragraph(app.config["MEDICAL_DISCLAIMER"], normal_style))

        doc.build(elements)
        buffer.seek(0)

        return send_file(
            buffer,
            mimetype="application/pdf",
            as_attachment=True,
            download_name="CareBridge_Report.pdf"
        )

    except Exception as e:
        logging.error(f"Report Error: {str(e)}")
        return jsonify({"error": "Report generation failed"}), 500


# --------------------------------
# RUN SERVER
# --------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)