# 🚑 CareBridge AI

## 🧠 Smart Health Risk Analyzer

CareBridge AI is an accessibility-first healthcare assistant that helps users analyze health risks using AI-style triage scoring based on symptoms and age.

It provides:
- 🎤 Voice symptom input
- 🌗 Dark / Light theme support
- 📊 Risk visualization dashboard
- ♿ Accessibility friendly UI
- 🚨 Emergency risk alerts

---

## ✨ Features

✅ AI-style health risk scoring engine  
✅ Real-time API backend using Flask  
✅ Voice symptom recognition  
✅ Animated risk meter visualization  
✅ Accessibility-first design  
✅ Sustainability health impact metric  

---

## 🏗 Project Structure
```
Carebridge-AI/        
├── README.md        
├── .gitignore (Python)        
├── Licence (MIT)        
├── app.py        
├── index.html        
├── style.css        
├── script.js
```

---

## 🚀 Setup Instructions

#### 1. Clone Repository
```
git clone https://github.com/yourusername/Carebridge-AI.git
cd Carebridge-AI
```

#### Install Dependencies
```pip install -r requirements.txt```

#### Run Backend
```gunicorn app:app

#### Open Frontend
```index.html

## 🌍 Deployment
**Backend:**  
Render / Railway / Railway-like platforms  
**Frontend:**  
GitHub Pages

## ❤️ Technologies Used:
- HTML5
- CSS3
- JavaScript
- Python Flask
- Flask-CORS

## 🐍 Backend API
#### Post ```/analyze```
** Request:**  
{  
  "symptoms": "fever cough",  
  "age": 25  
}  

**Response:**
{  
  "risk": "Low",  
  "confidence": 90,  
  "explanation": "Rest and hydrate"  
}  