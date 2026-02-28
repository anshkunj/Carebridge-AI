# 🚑 CareBridge AI — Accessibility First Health Risk Analyzer
**CareBridge AI** is an accessibility-focused health risk analysis system powered by AI-style symptom scoring and smart medical report generation.

The platform helps users:
- Analyze health risk from symptoms
- Generate professional medical PDF reports
- Receive AI-style medical insights
- Find nearby hospitals

Built using:
- Flask (Backend API)
- HTML + CSS + JavaScript (Frontend)
- ReportLab (PDF Medical Report Generation)

---

## 🚀 Features

✅ Health Risk Analysis Engine  
✅ AI-style Medical Insight Summary  
✅ Premium Medical Report PDF Generation  
✅ Voice Symptom Input Support  
✅ Dark / Light Theme UI  
✅ Accessibility Text Scaling  
✅ Hospital Location Finder  

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
├── requirements.txt  
└── render.yaml
```

---

## 🧠 Health Risk Logic

Risk is calculated using:

- Symptom severity scoring
- Age risk factors
- Emergency override detection

Risk Levels:
- 🟢 Low Risk
- 🟡 Moderate Risk
- 🔴 High Risk
- 🚨 Emergency Alert

## 🚀 Setup Instructions

#### Clone Repository

git clone ```https://github.com/anshkunj/Carebridge-AI.git```  
cd ```Carebridge-AI```

#### Install Dependencies
```pip install -r requirements.txt```

#### Run Backend
gunicorn app:app --bind 0.0.0.0:$PORT

#### Open Frontend
```index.html```

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
**Request:**  
{  
  "symptoms": "fever cough",  
  "age": 25  
}  

**Response:**
{  
  "risk": "Low",  
  "confidence": "75%",  
  "explanation": "Fever detected | Cough detected. Rest, hydrate and monitor symptoms"  
}  

#### Post ```/generate-report```
**returns:**
Medical PDF Report Download

>Try it live from the frontend: https://anshkunj.github.io/Carebridge-AI/

>Try it live from the backend: https://https://carebridge-backend-ro4e.onrender.com/

<p align="left">
  <a href="https://anshkunj.github.io/Portfolio" style="text-decoration: none;">
    <img 
      src="https://avatars.githubusercontent.com/u/254417216?v=4" 
      width="64" 
      style="border-radius: 6px; vertical-align: middle;"
    />
    <strong style="margin-left: 8px; font-size: 16px; vertical-align: middle;">
      anshkunj
    </strong>
  </a>
</p>

### 📫 Connect with me
[![GitHub](https://img.shields.io/badge/GitHub-anshkunj-black?style=flat&logo=github)](https://github.com/anshkunj)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-anshkunj-blue?style=flat&logo=linkedin)](https://linkedin.com/in/anshkunj)
[![Portfolio](https://img.shields.io/badge/Portfolio-Live-success?style=flat&logo=google-chrome)](https://anshkunj.github.io/Portfolio)
[![Discord](https://img.shields.io/badge/Discord-anshkunj-7289DA?style=flat&logo=discord)](https://discord.com/users/1473000023431057461)

### 🧠 Competitive Programming & Hackathons
[![LeetCode](https://img.shields.io/badge/LeetCode-anshkunj-orange?style=flat&logo=leetcode)](https://leetcode.com/u/anshkunj)
[![Codeforces](https://img.shields.io/badge/Codeforces-anshkunj-blue?style=flat&logo=codeforces)](https://codeforces.com/profile/anshkunj)
[![AtCoder](https://img.shields.io/badge/AtCoder-anshkunj-lightgrey?style=flat&logo=atcoder)](https://atcoder.jp/users/anshkunj)
[![HackerRank](https://img.shields.io/badge/HackerRank-anshkunj-brightgreen?style=flat&logo=hackerrank)](https://www.hackerrank.com/profile/anshkunj)
[![Devpost](https://img.shields.io/badge/Devpost-anshkunj-black?style=flat&logo=devpost)](https://devpost.com/anshkunj)

### 💼 Freelance Profiles
[![Fiverr](https://img.shields.io/badge/Fiverr-anshkunj-green?style=flat&logo=fiverr)](https://www.fiverr.com/anshkunj)
[![Freelancer](https://img.shields.io/badge/Freelancer-anshkunj-blue?style=flat&logo=freelancer)](https://www.freelancer.com/u/anshkunj)

---

### ⭐ Support
If you found this project helpful, consider giving it a ⭐  
It motivates me to build more real-world, production-ready projects 🚀

---

### 📝 Note
This repository is regularly updated with new scripts and improvements.