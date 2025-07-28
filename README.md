# 🎓 Student Math Score Prediction (End-to-End ML Project)

This project is an end-to-end machine learning pipeline that predicts a student's **math score** based on features such as **reading score**, **writing score**, **gender**, **race/ethnicity**, **lunch type**, and **test preparation course**. The application is fully deployed on **Google Cloud Platform (GCP)** using **Cloud Build** and **Cloud Run**.

---

## 🔍 Objective

To accurately predict the math scores of students using other performance metrics and demographic features. This project demonstrates full-cycle ML workflow: from data preprocessing and modeling to frontend integration and cloud deployment.

---

## 🧰 Tech Stack

* **Languages**: Python
* **ML Libraries**: Scikit-learn, XGBoost
* **Data Tools**: Pandas, NumPy
* **Web & UI**: Flask, TailwindCSS, Jinja2 templates
* **Visualization**: Matplotlib, Seaborn
* **Deployment**: Docker, Google Cloud Platform (Cloud Run, Cloud Build)

---

## 📂 Folder Structure

```
project-root/
├── artifacts/             # Saved models, logs, etc.
├── notebooks/             # EDA and training notebooks
├── src/                   # ML pipeline scripts
├── static/css/            # Tailwind-generated CSS
├── tailwind/              # Tailwind config and source
├── templates/             # HTML templates for web interface
├── .dockerignore
├── .gitignore
├── Dockerfile             # For containerization
├── README.md              # This file
├── app.py                 # Flask application entry
├── cloudbuild.yaml        # CI/CD pipeline config for GCP
├── requirements.txt       # Python dependencies
├── run.py                 # Alternate entry point
├── setup.py               # Setup config for installation
```

---

## 🔢 Dataset Overview

* Based on a publicly available educational dataset (synthetic/academic use)
* Features include:

  * `gender`
  * `race/ethnicity`
  * `parental level of education`
  * `lunch`
  * `test preparation course`
  * `reading score`
  * `writing score`
* **Target Variable**: `math score`

---

## ⚖️ Model Pipeline

1. **Data Cleaning**: Handle missing values, encoding categorical variables
2. **Feature Engineering**: Convert categories, scale numeric features
3. **EDA**: Explore distributions and correlations
4. **Modeling**: Trained models like Linear Regression, Random Forest, XGBoost
5. **Evaluation**: RMSE, R² score
6. **Export**: Save best model to artifacts/

---

## 🚀 Deployment on Google Cloud Platform

### CI/CD using Cloud Build & Cloud Run

1. Dockerized the application using `Dockerfile`
2. Configured automated deployment with `cloudbuild.yaml`
3. Pushed to GCP and deployed with Cloud Run (fully managed)

#### Manual Commands (if needed):

```bash
gcloud builds submit --tag gcr.io/<project-id>/math-score-app
gcloud run deploy math-score-app \
  --image gcr.io/<project-id>/math-score-app \
  --platform managed \
  --region <your-region> \
  --allow-unauthenticated
```

---

## ✅ Results

* Achieved strong performance with regression metrics (R² \~0.92+)
* Reading and writing scores were highly correlated with math performance
* User-friendly UI to input student features and see predicted score instantly

---

## 🙌 Acknowledgments

* [UCI ML Repository (Student Dataset)](https://archive.ics.uci.edu/)
* Google Cloud Free Tier for deployment
* TailwindCSS for styling

---

## 💼 License

MIT License — for educational and demonstration purposes only
