# stress-typing-app
This project is a web-based application that predicts a user's stress level based on their typing behaviour. The system captures keystroke dynamics such as typing speed, pause duration, and backspace usage, and uses a machine learning model to classify stress levels as Low, Medium, or High
# Stress Prediction Using Typing Behaviour

## Nexora Hacks 2026 Submission


## 🧠 Problem Statement
Stress often goes unnoticed in students and professionals until it negatively impacts performance, productivity, and mental well-being. Traditional stress detection methods are intrusive or require manual input. However, behavioral patterns such as typing speed, pauses, and error rates can act as indirect indicators of stress.


## 💡 Solution
This project is a web-based application that predicts a user's stress level based on their typing behaviour. The system captures keystroke dynamics such as typing speed, pause duration, and backspace usage, and uses a machine learning model to classify stress levels as **Low**, **Medium**, or **High**.

The solution is non-intrusive, easy to use, and provides instant feedback.



## ⚙️ Features
- Real-time typing behaviour capture
- Stress level prediction using Machine Learning
- Simple and intuitive web interface
- Non-intrusive stress detection
- Beginner-friendly and explainable model



## 🛠️ Technologies Used
- **Python**
- **Flask**
- **Scikit-learn**
- **NumPy**
- **HTML, CSS, JavaScript**
- **Machine Learning (Logistic Regression / Random Forest)**



## 📂 Project Structure


stress-typing-app/
│
├── app.py
├── model.py
├── requirements.txt
│
├── templates/
│   └── index.html
│
└── static/
├── script.js
└── style.css



## 🚀 How to Run the Project Locally

### 1️⃣ Clone the Repository
git clone <your-repository-link>
cd stress-typing-app

### 2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate

### 3️⃣ Install Dependencies
pip install -r requirements.txt

### 4️⃣ Run the Application
python app.py

### 5️⃣ Open in Browser
http://127.0.0.1:5000/


## 📊 Machine Learning Approach

* Features used:

  * Typing speed (keys per second)
  * Average pause duration
  * Error rate (backspace usage)
* A lightweight ML model is trained using a synthetic dataset to simulate stress patterns.
* The model outputs stress levels: **Low**, **Medium**, or **High**.



## 📈 Future Improvements

* Use real-world typing datasets for better accuracy
* Add real-time stress monitoring dashboard
* Integrate wellness recommendations and alerts
* Deploy as a browser extension or mobile app


## 🏆 Hackathon Alignment

* **Creativity:** Behavioral stress detection using typing patterns
* **Real World Use:** Applicable in workplaces and educational environments
* **Technologies Used:** AI/ML + Web Application


## 📌 Note

This project was built as part of **Nexora Hacks 2026**. AI-assisted development tools were used to accelerate prototyping while focusing on system design, feature engineering, and real-world applicability.


## 👤 Author

**STUTI SHARMA**

