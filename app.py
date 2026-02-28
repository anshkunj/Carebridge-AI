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
    
@app.route("/")    
def landing():    
    
    return """    
    <!DOCTYPE html>    
    <html>    
    <head>    
        <title>CareBridge AI</title>    
    
        <style>    
            body{    
                margin:0;    
                height:100vh;    
                display:flex;    
                justify-content:center;    
                align-items:center;    
                background:linear-gradient(135deg,#0f172a,#020617);    
                color:white;    
                font-family:Segoe UI,sans-serif;    
                text-align:center;    
                animation:fadeIn 1.5s ease;    
            }    
    
            .box{    
                padding:40px;    
                border-radius:25px;    
                background:rgba(255,255,255,0.05);    
                backdrop-filter:blur(20px);    
                box-shadow:0 20px 60px rgba(0,0,0,.5);    
            }    
    
            a{    
                display:inline-block;    
                margin-top:20px;    
                padding:14px 30px;    
                background:#38bdf8;    
                color:black;    
                text-decoration:none;    
                border-radius:12px;    
                font-weight:bold;    
            }    
    
            a:hover{    
                transform:scale(1.05);    
            }    
    
            @keyframes fadeIn{    
                from{opacity:0; transform:translateY(20px);}    
                to{opacity:1; transform:translateY(0);}    
            }    
    
        </style>    
    </head>    
    
    <body>    
    
        <div class="box">    
            <h1>🚑 CareBridge AI</h1>    
            <p>Accessibility First Health Risk Analyzer</p>    
    
            <a href="https://anshkunj.github.io/Carebridge-AI">    
                🌍 Open CareBridge Frontend    
            </a>    
        </div>    
    
    </body>    
    </html>    
    """    
    
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
