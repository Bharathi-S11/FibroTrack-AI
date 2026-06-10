# FibroTrack AI 🩺

### AI-Powered Liver Fibrosis Stage Prediction and Personalized Indian Diet Recommendation

## 📌 Project Overview

FibroTrack AI is a machine learning-based web application designed to predict the stage of liver fibrosis using patient clinical parameters. The system provides an early risk assessment along with confidence and risk percentage scores and generates personalized Indian diet recommendations based on the predicted fibrosis stage and patient's age.

The project aims to support healthcare awareness and demonstrate the application of Artificial Intelligence in preventive healthcare. It is intended for educational and research purposes and should not be considered a replacement for professional medical diagnosis.

---

## 🎯 Objectives

* Predict liver fibrosis stages (F0–F4) using machine learning.
* Provide prediction confidence and risk percentage.
* Generate personalized Indian diet plans.
* Visualize important health parameters.
* Build an easy-to-use web interface for users.

---

## ✨ Features

* ✅ Liver Fibrosis Stage Prediction (F0–F4)
* ✅ Confidence Score Calculation
* ✅ Risk Percentage Estimation
* ✅ Personalized Indian Diet Recommendation
* ✅ Interactive Streamlit Web Application
* ✅ Data Visualization with Heatmaps and Charts
* ✅ User-Friendly Interface

---

## 🛠️ Technologies Used

| Category                | Technology                         |
| ----------------------- | ---------------------------------- |
| Programming Language    | Python                             |
| Machine Learning        | Scikit-learn                       |
| Data Processing         | Pandas, NumPy                      |
| Data Visualization      | Matplotlib, Seaborn                |
| Model                   | Logistic Regression, Random Forest |
| Web Framework           | Streamlit                          |
| Development Environment | Google Colab, VS Code              |
| Version Control         | Git & GitHub                       |

---

## 📂 Project Structure

```
FibroTrack-AI/
│
├── indian_liver_patient.csv(Dataset)
├── models/
│   ├── logistic_model.pkl
│   └── random_forest_model.pkl
├── app.py
├── README.md
└── assets/

```

---

## 📊 Workflow

1. Data Collection
2. Data Preprocessing
3. Exploratory Data Analysis
4. Feature Selection
5. Model Training
6. Model Evaluation
7. Liver Fibrosis Stage Prediction
8. Confidence & Risk Score Calculation
9. Personalized Diet Recommendation
10. Streamlit Deployment

---

## 🩺 Liver Fibrosis Stages

| Stage  | Description                 |
| ------ | --------------------------- |
| **F0** | No Fibrosis (Healthy Liver) |
| **F1** | Mild Fibrosis               |
| **F2** | Moderate Fibrosis           |
| **F3** | Advanced Fibrosis           |
| **F4** | Severe Fibrosis (Cirrhosis) |

---

## 📈 Machine Learning Models

### Logistic Regression

* Used as a baseline classification model.
* Provides interpretable predictions.
* Fast and efficient for binary classification.

### Random Forest

* Ensemble learning algorithm.
* Improves prediction accuracy.
* Handles complex relationships between clinical features.

---

## 🥗 Personalized Diet Recommendation

Based on the predicted fibrosis stage and age, FibroTrack AI recommends:

* Breakfast
* Lunch
* Dinner
* Healthy Snacks
* Hydration Tips

The diet focuses on balanced Indian meals that support liver health and healthy lifestyle habits.

---

## 📊 Evaluation Metrics

* Accuracy
* Precision
* Recall
* F1-Score
* Confusion Matrix
* ROC-AUC Score

---

## 🚀 Installation

```bash
git clone https://github.com/your-username/FibroTrack-AI.git

cd FibroTrack-AI

pip install -r requirements.txt

streamlit run app.py
```

---

## 📷 Project Screenshots

Add screenshots of:

* Home Page & Prediction Result
  <img width="1920" height="1080" alt="Screenshot 2026-05-06 183025" src="https://github.com/user-attachments/assets/89e70398-af4e-415c-830e-a4a0b07b5f2a" />


* Diet Recommendation
  <img width="1920" height="1080" alt="Screenshot 2026-05-17 135715" src="https://github.com/user-attachments/assets/5c67bba4-acf8-4c98-9b80-456bf0b1b153" />


* Report in PDF
  <img width="1226" height="693" alt="Screenshot 2026-05-14 210409" src="https://github.com/user-attachments/assets/83e28394-4088-4b85-a0ff-8b694700f5ca" />


---

## 🔮 Future Enhancements

* Deep Learning Models
* SHAP Explainable AI Integration
* PDF Health Report Generation
* Doctor Dashboard
* Cloud Deployment
* Multi-language Support
* Electronic Health Record (EHR) Integration

---


## 👨‍💻 Author

**Bharathi S**

AI & Data Science Student

**Project:** FibroTrack AI – AI-Powered Liver Fibrosis Stage Prediction and Personalized Indian Diet Recommendation

---

## ⭐ Support

If you found this project helpful, consider giving it a **⭐ Star** on GitHub and sharing your feedback!
