# 🛰️ CORE AI: Predictive Maintenance System

## 🚀 Live Links
* **Web Interface:** [Live Demo - Streamlit App](https://maintenance-prediction-ai.streamlit.app/)

---

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-%233F4F75.svg?style=for-the-badge&logo=plotly&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626.svg?style=for-the-badge&logo=Jupyter&logoColor=white)

A high-performance neural diagnostic interface that leverages Machine Learning to predict industrial machine failures before they happen. Designed with a futuristic, cyber-industrial aesthetic, this tool processes real-time sensor telemetry to deliver accurate reliability indices and AI-driven maintenance prescriptions.

## ✨ Features

* **🔮 Predictive Engine:** Powered by a Random Forest Classifier trained on industrial machine telemetry to predict failure probabilities.
* **🧪 Complete ML Pipeline:** Includes a fully documented Jupyter Notebook detailing the Exploratory Data Analysis (EDA), feature engineering, and model training processes.
* **🎛️ High-End UI:** Custom CSS featuring glassmorphism, neon-glow accents, and a dark-mode industrial aesthetic.
* **📊 Advanced Data Visualization:** * **Probability Gauge:** Real-time risk assessment meter.
  * **Sensor Fingerprint (Radar Chart):** Multidimensional view of current machine stress parameters.
* **🤖 AI Prescriptions:** Actionable, context-aware recommendations (e.g., immediate motor load decrease, tool replacement, or cooling system checks) based on specific parameter thresholds.

## 🛠️ Tech Stack

* **Frontend & Deployment:** Streamlit (Community Cloud)
* **Backend API:** FastAPI (Model Serving)
* **Machine Learning:** Scikit-Learn, Pandas, NumPy, Joblib
* **Data Visualization:** Plotly Graph Objects
* **Development:** Jupyter Notebook

## 📂 Repository Structure

```text
├── ui.py                              # Main Streamlit application frontend
├── app_maintenance.py                 # Backend API for the model (FastAPI)
├── full_ML_pipeline.ipynb             # Complete ML workflow (EDA, Training, Evaluation)
├── predictive_maintenance_model.pkl   # Pre-trained Random Forest model
├── requirements.txt                   # Project dependencies
└── README.md                          # Project documentation
