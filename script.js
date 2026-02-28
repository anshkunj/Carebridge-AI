const form = document.getElementById("healthForm");

const analyzeBtn = document.querySelector("button[type='submit']");
const reportBtn = document.querySelector(".report-btn");

/* ===============================
   COMMON VALIDATION ENGINE
================================ */

function validateInputs(){

const symptoms = document.getElementById("symptoms").value.trim();
const age = document.getElementById("age").value.trim();

if(!symptoms){
alert("Please enter symptoms");
return false;
}

if(!age){
alert("Please enter age");
return false;
}

return true;
}

/* ===============================
   ANALYZE RISK
================================ */

form.addEventListener("submit", async e=>{

e.preventDefault();

if(!validateInputs()) return;

const symptoms = document.getElementById("symptoms").value;
const age = document.getElementById("age").value;

const resultBox = document.getElementById("report");
const riskText = document.getElementById("riskText");
const riskBar = document.getElementById("riskBar");

/* Loading UI */

riskText.innerText = "Analyzing symptoms...🧐";
resultBox.innerText = "Processing health risk analysis...";

try{

analyzeBtn.disabled = true;

const res = await fetch(
"https://carebridge-backend-ro4e.onrender.com/analyze",
{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({symptoms, age})
});

const data = await res.json();

/* Result Display */

riskText.innerText =
`Risk : ${data.risk} | Confidence : ${data.confidence}%`;

resultBox.innerText = data.explanation;

/* Risk Bar */

let width = 30;

if(data.risk === "Low") width = 30;
else if(data.risk === "Moderate") width = 60;
else width = 90;

riskBar.style.width = width + "%";

/* Risk Color */

riskText.className = "";

if(data.risk === "Low")
riskText.classList.add("risk-low");

else if(data.risk === "Moderate")
riskText.classList.add("risk-medium");

else
riskText.classList.add("risk-high");

/* Hospital Suggestion */

const hospitalBtn = document.getElementById("hospitalBtn");

if(hospitalBtn && data.hospital_map){
hospitalBtn.href = data.hospital_map;
hospitalBtn.style.display = "inline-block";
}

}
catch(err){

resultBox.innerText =
"Error analyzing symptoms";

console.error(err);

}
finally{
analyzeBtn.disabled = false;
}

});


/* ===============================
   THEME TOGGLE
================================ */

function toggleTheme(){

document.body.classList.toggle("light-theme");

if(document.body.classList.contains("light-theme")){
localStorage.setItem("theme","light");
}else{
localStorage.setItem("theme","dark");
}

}

window.onload = ()=>{

if(localStorage.getItem("theme")==="light"){
document.body.classList.add("light-theme");
}

};


/* ===============================
   TEXT SIZE
================================ */

function toggleText(){
document.body.classList.toggle("large-text");
}


/* ===============================
   VOICE INPUT
================================ */

function startVoice(){

const SpeechRecognition =
window.SpeechRecognition ||
window.webkitSpeechRecognition;

if(!SpeechRecognition){
alert("Voice input not supported");
return;
}

const recognition = new SpeechRecognition();
recognition.start();

recognition.onresult = e=>{
document.getElementById("symptoms").value =
e.results[0][0].transcript;
};

}


/* ===============================
   REPORT GENERATOR
================================ */

async function generateReport(){

if(!validateInputs()) return;

const symptoms = document.getElementById("symptoms").value.trim();
const age = document.getElementById("age").value;

try{

reportBtn.disabled = true;
reportBtn.innerText = "Generating Report... 📄";

const res = await fetch(
"https://carebridge-backend-ro4e.onrender.com/generate-report",
{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({symptoms, age})
});

const blob = await res.blob();

const url = window.URL.createObjectURL(blob);

const a = document.createElement("a");
a.href = url;
a.download = "CareBridge_Report.pdf";
a.click();

}
catch(err){
alert("Report generation failed");
console.error(err);
}
finally{
reportBtn.disabled = false;
reportBtn.innerText = "📄 Download Health Report";
}

}