from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# Startup AI Medical Intelligence Engine
def ai_triage_engine(symptoms, age):

    symptoms = symptoms.lower()

    risk_score = 0

    # Medical pattern intelligence
    severity_words = ["severe","extreme","unbearable","very bad"]
    emergency_words = ["unconscious","bleeding","heart attack","paralyzed"]

    # Pattern detection
    if any(w in symptoms for w in emergency_words):
        risk_score += 10

    if "fever" in symptoms: risk_score += 2
    if "cough" in symptoms: risk_score += 2
    if "chest pain" in symptoms: risk_score += 6
    if "breathing" in symptoms: risk_score += 6
    if age > 60: risk_score += 3

    # Startup style probability scoring
    probability = min(98, risk_score * 10 + random.randint(5,15))

    if probability < 40:
        risk="Low"
        advice="Rest + hydration recommended"

    elif probability < 75:
        risk="Moderate"
        advice="Monitor symptoms and consult doctor"

    else:
        risk="High"
        advice="🚨 Seek immediate medical attention"

    sustainability_score = max(0,100-probability)

    return risk, probability, advice, sustainability_score


@app.route("/")
def index():
    return """
    <html>
    <head>
        <meta http-equiv="refresh" content="2; url=https://anshkunj.github.io/carebridge-ai/" />

        <style>
            body{
                background:#0f172a;
                color:white;
                font-family:Segoe UI;
                display:flex;
                justify-content:center;
                align-items:center;
                height:100vh;
                flex-direction:column;
                text-align:center;
            }

            .loader{
                width:60px;
                height:60px;
                border-radius:50%;
                border:6px solid #38bdf8;
                border-top-color:transparent;
                animation:spin 1s linear infinite;
                margin-bottom:20px;
            }

            @keyframes spin{
                to{ transform:rotate(360deg); }
            }

            h2{
                color:#38bdf8;
            }
        </style>
    </head>

    <body>

        <div class="loader"></div>

        <h2>🚑 CareBridge AI Loading...</h2>
        <p>Redirecting to Health Assistant Portal</p>

    </body>
    </html>
    """

@app.route("/analyze", methods=["POST"])
def analyze():

    data=request.get_json()

    symptoms=data.get("symptoms","")
    age=int(data.get("age",0))

    risk,probability,advice,sustainability = ai_triage_engine(symptoms,age)

    return jsonify({
        "risk":risk,
        "confidence":probability,
        "explanation":advice,
        "sustainability":sustainability
    })


if __name__=="__main__":
    app.run()