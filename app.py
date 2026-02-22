from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def analyze_health(symptoms, age):

    symptoms = symptoms.lower()
    score = 0

    if "fever" in symptoms: score+=2
    if "cough" in symptoms: score+=2
    if "breathing" in symptoms: score+=5
    if "chest pain" in symptoms: score+=5

    if age >= 60: score+=3
    if age <= 5: score+=2

    if score<=3:
        risk="Low"
        advice="Rest and hydrate"

    elif score<=7:
        risk="Moderate"
        advice="Monitor symptoms"

    else:
        risk="High"
        advice="Seek medical help immediately"

    return {
        "risk":risk,
        "confidence":90,
        "explanation":advice,
        "sustainability":100-(score*10)
    }

@app.route("/analyze",methods=["POST"])
def analyze():
    data=request.json
    return jsonify(
        analyze_health(
            data.get("symptoms",""),
            int(data.get("age",0))
        )
    )

if __name__=="__main__":
    app.run()