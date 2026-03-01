# --------------------------------
# HEALTH ANALYSIS ENGINE
# --------------------------------

def analyze_health(symptoms, age, location=""):

    symptoms = (symptoms or "").lower().strip()
    score = 0
    explanation_list = []

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

    # Detect symptoms
    for symptom, weight in symptom_weights.items():
        if symptom in symptoms:
            score += weight
            explanation_list.append(f"{symptom.title()} detected")

    # Age Risk Factors
    if age >= 60:
        score += 4
        explanation_list.append("Senior age risk factor")

    if 0 < age <= 5:
        score += 3
        explanation_list.append("Child age risk factor")

    # --------------------------------
    # Google Maps Hospital Link
    # --------------------------------
    hospital_map = ""

    if location:
        hospital_map = (
            "https://www.google.com/maps/search/?api=1&query=hospitals+near+"
            + location.replace(" ", "+")
        )

    # --------------------------------
    # Emergency Override
    # --------------------------------
    if "chest pain" in symptoms or "emergency" in symptoms:
        return {
            "risk": "EMERGENCY",
            "confidence": 95,
            "explanation": "Critical symptom detected. Seek emergency medical help immediately.",
            "hospital_map": hospital_map
        }

    # --------------------------------
    # Risk Classification
    # --------------------------------
    if score <= 4:
        risk = "Low"
        advice = "Rest, hydrate and monitor symptoms."

    elif score <= 10:
        risk = "Moderate"
        advice = "Consult a doctor if symptoms persist."

    else:
        risk = "High"
        advice = "Medical consultation strongly recommended."

    confidence = min(98, 65 + (score * 2.5))

    explanation_text = " | ".join(explanation_list)
    if explanation_text:
        explanation_text += ". "
    explanation_text += advice

    return {
        "risk": risk,
        "confidence": round(confidence, 2),
        "explanation": explanation_text,
        "hospital_map": hospital_map
    }


# --------------------------------
# SUSTAINABILITY ENGINE
# --------------------------------

def calculate_green_score(risk):

    if risk == "Low":
        return 90
    elif risk == "Moderate":
        return 60
    elif risk == "High":
        return 25
    elif risk == "EMERGENCY":
        return 5
    else:
        return 0


def estimate_environmental_impact(risk):

    if risk == "Low":
        return {"co2_saved": 4.5, "paper_saved": 1}

    elif risk == "Moderate":
        return {"co2_saved": 2.0, "paper_saved": 0.5}

    elif risk == "High":
        return {"co2_saved": 0.5, "paper_saved": 0}

    else:
        return {"co2_saved": 0, "paper_saved": 0}


# --------------------------------
# MEDICAL SUMMARY ENGINE
# --------------------------------

def generate_medical_summary(result):

    risk = result.get("risk", "Unknown")

    if risk == "Low":
        return (
            "Low health risk detected. Preventive care reduces unnecessary "
            "hospital visits and environmental impact."
        )

    elif risk == "Moderate":
        return (
            "Moderate risk detected. Early consultation recommended "
            "to prevent condition escalation."
        )

    elif risk == "High":
        return (
            "High risk symptoms detected. Immediate medical consultation "
            "strongly recommended."
        )

    elif risk == "EMERGENCY":
        return (
            "Emergency symptoms detected. Seek immediate medical help."
        )

    else:
        return "Health status could not be determined."