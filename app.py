"""
CS210 Final Project - Heart Disease Prediction Streamlit App
Interactive web application for real-time heart disease risk assessment
Authors: Aditya Baranwal, Kayla Nadolny, Anupam Pradeep
Date: July 2025
GitHub: https://github.com/AdityaBaranwal1/heart-disease-risk-predictor
"""

import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Heart Disease Risk Predictor",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #d63384;
        text-align: center;
        margin-bottom: 2rem;
    }
    .cs210-badge {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        text-align: center;
        margin: 1rem 0;
    }
    .risk-high {
        background-color: #dc3545;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    .risk-moderate {
        background-color: #fd7e14;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    .risk-low {
        background-color: #28a745;
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<h1 class="main-header"> Heart Disease Risk Predictor</h1>', unsafe_allow_html=True)
st.markdown('<div class="cs210-badge">CS210 Final Project - Machine Learning for Healthcare</div>', unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page:", [
    "🏠 Risk Assessment",
    " Model Performance",
    " Feature Analysis",
    " About CS210 Project"
])

# API endpoint
API_URL = "http://localhost:5000"

def make_prediction(patient_data):
    """Make prediction using the API."""
    try:
        response = requests.post(f"{API_URL}/predict", json=patient_data, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            return {"success": False, "error": f"API Error: {response.status_code}"}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Cannot connect to API. Please ensure the API server is running on localhost:5000"}
    except Exception as e:
        return {"success": False, "error": str(e)}

if page == "🏠 Risk Assessment":
    st.header("Enter Patient Information")
    st.markdown("*Fill in the clinical data below to assess heart disease risk*")

    # Create input form
    with st.form("patient_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("Demographics")
            age = st.number_input("Age (years)", min_value=0, max_value=120, value=67)
            sex = st.selectbox("Gender", [0, 1], format_func=lambda x: "Female" if x == 0 else "Male", index=1)

            st.subheader("Vital Signs")
            trestbps = st.number_input("Resting Blood Pressure (mmHg)", min_value=50, max_value=300, value=160)
            chol = st.number_input("Cholesterol (mg/dl)  KEY FEATURE", min_value=0, max_value=600, value=286)

        with col2:
            st.subheader("Symptoms & Tests")
            cp = st.selectbox("Chest Pain Type", [0, 1, 2, 3],
                            format_func=lambda x: ["Asymptomatic", "Atypical Angina", "Non-Anginal Pain", "Typical Angina"][x], index=0)
            fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", [0, 1],
                             format_func=lambda x: "False" if x == 0 else "True", index=0)
            restecg = st.selectbox("Resting ECG", [0, 1, 2],
                                 format_func=lambda x: ["Normal", "ST-T Abnormality", "LV Hypertrophy"][x], index=2)
            exang = st.selectbox("Exercise Induced Angina", [0, 1],
                               format_func=lambda x: "No" if x == 0 else "Yes", index=1)

        with col3:
            st.subheader("Exercise Test Results")
            thalch = st.number_input("Max Heart Rate  KEY FEATURE", min_value=50, max_value=250, value=108)
            oldpeak = st.number_input("ST Depression", min_value=0.0, max_value=10.0, value=1.5, step=0.1)
            slope = st.selectbox("ST Slope", [0, 1, 2],
                                format_func=lambda x: ["Upsloping", "Flat", "Downsloping"][x], index=1)
            ca = st.number_input("Major Vessels (0-4)", min_value=0, max_value=4, value=3)
            thal = st.selectbox("Thalassemia", [0, 1, 2, 3],
                              format_func=lambda x: ["Normal", "Fixed Defect", "Reversible Defect", "Unknown"][x], index=0)

        submitted = st.form_submit_button(" Assess Risk", use_container_width=True)

        if submitted:
            # Prepare data
            patient_data = {
                'age': age, 'sex': sex, 'cp': cp, 'trestbps': trestbps, 'chol': chol,
                'fbs': fbs, 'restecg': restecg, 'thalach': thalch, 'exang': exang,
                'oldpeak': oldpeak, 'slope': slope, 'ca': ca, 'thal': thal
            }

            # Make prediction
            with st.spinner("Analyzing patient data..."):
                result = make_prediction(patient_data)

            if result.get('success'):
                st.header(" Risk Assessment Results")

                col1, col2 = st.columns(2)

                with col1:
                    # Risk level display
                    risk_level = result['risk_level']
                    disease_prob = result['probability_disease']

                    if 'Very High' in risk_level or 'High' in risk_level:
                        st.markdown(f'<div class="risk-high"><h3>Risk Level: {risk_level}</h3><h2>{disease_prob:.1%} Disease Probability</h2></div>',
                                  unsafe_allow_html=True)
                    elif 'Moderate' in risk_level:
                        st.markdown(f'<div class="risk-moderate"><h3>Risk Level: {risk_level}</h3><h2>{disease_prob:.1%} Disease Probability</h2></div>',
                                  unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="risk-low"><h3>Risk Level: {risk_level}</h3><h2>{disease_prob:.1%} Disease Probability</h2></div>',
                                  unsafe_allow_html=True)

                    # Recommendation
                    st.subheader(" Recommendation")
                    st.info(result['recommendation'])

                    # Model info
                    st.subheader("🤖 Model Information")
                    st.write(f"**Model Used:** {result['model_used']}")
                    st.write(f"**Confidence:** {result['confidence']:.1%}")

                with col2:
                    # Risk factors
                    if result.get('key_risk_factors'):
                        st.subheader(" Key Risk Factors Identified")
                        for factor in result['key_risk_factors']:
                            st.warning(factor)

                    # Probability gauge
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = disease_prob * 100,
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "Disease Risk %"},
                        gauge = {'axis': {'range': [None, 100]},
                                'bar': {'color': "darkred"},
                                'steps': [
                                    {'range': [0, 25], 'color': "lightgreen"},
                                    {'range': [25, 50], 'color': "yellow"},
                                    {'range': [50, 75], 'color': "orange"},
                                    {'range': [75, 100], 'color': "red"}],
                                'threshold': {'line': {'color': "black", 'width': 4},
                                            'thickness': 0.75, 'value': 90}}))
                    fig.update_layout(height=300)
                    st.plotly_chart(fig, use_container_width=True)

            else:
                st.error(f"Prediction failed: {result.get('error', 'Unknown error')}")

elif page == " Model Performance":
    st.header("CS210 Model Evaluation Results")

    # Get model performance from API
    try:
        response = requests.get(f"{API_URL}/model_performance", timeout=10)
        if response.status_code == 200:
            perf_data = response.json()

            # Performance comparison
            st.subheader("Model Comparison (CS210 Evaluation)")

            models = list(perf_data['cs210_evaluation'].keys())
            metrics = ['accuracy', 'precision', 'recall', 'roc_auc']

            # Create comparison chart
            fig = go.Figure()
            for metric in metrics:
                values = [perf_data['cs210_evaluation'][model][metric] for model in models]
                fig.add_trace(go.Bar(name=metric.upper(), x=models, y=values))

            fig.update_layout(
                title="Model Performance Comparison",
                xaxis_title="Models",
                yaxis_title="Score",
                barmode='group',
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)

            # Performance table
            st.subheader("Detailed Performance Metrics")
            df = pd.DataFrame(perf_data['cs210_evaluation']).T
            st.dataframe(df.style.highlight_max(axis=0))

            # Methodology
            st.subheader("Evaluation Methodology")
            methodology = perf_data['methodology']
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Train/Test Split:** {methodology['train_test_split']}")
                st.write(f"**Cross Validation:** {methodology['cross_validation']}")
            with col2:
                st.write(f"**Feature Selection:** {methodology['feature_selection']}")
                st.write(f"**Preprocessing:** {methodology['preprocessing']}")

        else:
            st.error("Could not load model performance data")
    except:
        st.error("API connection failed. Please ensure the API is running.")

elif page == " Feature Analysis":
    st.header("Feature Importance Analysis")

    try:
        response = requests.get(f"{API_URL}/feature_importance", timeout=10)
        if response.status_code == 200:
            feature_data = response.json()

            # Feature importance chart
            st.subheader("Random Forest Feature Importance (CS210)")

            features = list(feature_data['feature_importance'].keys())
            importance = list(feature_data['feature_importance'].values())

            fig = px.bar(x=importance, y=features, orientation='h',
                        title="Feature Importance Scores",
                        labels={'x': 'Importance Score', 'y': 'Features'})
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)

            # Top features
            st.subheader(" Key Findings from CS210 Analysis")
            col1, col2, col3 = st.columns(3)

            top_features = feature_data['top_3_features']
            findings = feature_data['cs210_findings']

            with col1:
                st.metric("Top Feature", top_features[0].title(), "15% importance")
                st.info(findings[top_features[0]])

            with col2:
                st.metric("Second Feature", top_features[1].title(), "14% importance")
                st.info(findings[top_features[1]])

            with col3:
                st.metric("Third Feature", top_features[2].title(), "12% importance")
                st.info(findings[top_features[2]])

        else:
            st.error("Could not load feature importance data")
    except:
        st.error("API connection failed. Please ensure the API is running.")

elif page == " About CS210 Project":
    st.header("CS210 Final Project - Heart Disease Prediction")

    try:
        response = requests.get(f"{API_URL}/streamlit_info", timeout=10)
        if response.status_code == 200:
            project_info = response.json()

            col1, col2 = st.columns(2)

            with col1:
                st.subheader(" Project Overview")
                st.write("**Authors:** Aditya Baranwal, Kayla Nadolny, Anupam Pradeep")
                st.write("**Course:** CS210 - Data Management for Data Science")
                st.write("**Date:** July 2025")
                st.write("**GitHub:** https://github.com/AdityaBaranwal1/heart-disease-risk-predictor")

                st.subheader(" Project Goals")
                st.write("- Predict heart disease risk using machine learning")
                st.write("- Compare multiple ML algorithms")
                st.write("- Create interactive web application")
                st.write("- Enable early detection for better outcomes")

                st.subheader(" Dataset")
                st.write("- **Source:** UCI Heart Disease Dataset")
                st.write("- **Preprocessing:** Outlier removal, encoding, imputation")
                st.write("- **Features:** 13 clinical indicators")
                st.write("- **Target:** Binary classification (disease/no disease)")

            with col2:
                st.subheader(" Key Achievements")
                conclusion = project_info['cs210_conclusion']

                st.success(f"**Best Models:** {', '.join(conclusion['best_models'])}")
                st.success(f"**Key Features:** {', '.join(conclusion['key_features'])}")
                st.info(conclusion['early_detection'])
                st.info(conclusion['accessibility'])

                st.subheader(" Deployment Strategy")
                deployment = project_info['streamlit_app']['deployment']

                st.write(f"**Local:** `python cs210_launcher.py`")
                st.write(f"**Future:** {deployment['future']}")
                st.write(f"**Goal:** {deployment['goal']}")

                st.subheader(" Technical Stack")
                st.write("- **ML:** scikit-learn, pandas, numpy")
                st.write("- **Models:** Logistic Regression, Random Forest, Gradient Boosting")
                st.write("- **Web:** Streamlit, Flask API")
                st.write("- **Visualization:** Plotly, matplotlib, seaborn")

        else:
            st.error("Could not load project information")
    except:
        st.error("API connection failed. Please ensure the API is running.")

# Footer
st.markdown("---")
st.markdown("**CS210 Final Project** | Heart Disease Prediction with Machine Learning | July 2025")
st.markdown("**Authors:** Aditya Baranwal, Kayla Nadolny, Anupam Pradeep")
st.markdown("*This application demonstrates machine learning techniques for healthcare applications*")
