# Digital-Phenotyping-Positive-Emotions

# Psychological State Prediction from Wearable Sensor Data

This repository contains the codebase for the manuscript:

**"Predicting Daily Psychological States from Wearable Sensor Data Using Machine Learning and Explainable AI"**  
Submitted to *PLOS ONE*, 2025.

The project aims to predict 18 daily psychological states (e.g., positive/negative affect, self-esteem, meaning in life, personal relationships) from multimodal wearable sensor data collected over 8 days using Empatica EmbracePlus devices.

---

## 🧠 Key Features

- Preprocessing of raw physiological data (ACC, EDA, PRV/IBI).
- Feature extraction using the FLIRT toolkit.
- Data imputation, standardization, and dimensionality reduction (PCA).
- Training and evaluation of various ML models (Random Forest, XGBoost, LightGBM, CNN, LSTM).
- Explainable AI analyses using SHAP and MAPIE for interpretability and uncertainty quantification.
