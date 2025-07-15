"""
Improved Web Interface for Heart Disease Severity Prediction
Shows both binary classification and severity levels (0-4)
"""

import requests
from flask import Flask, render_template, request, flash, redirect, url_for

app = Flask(__name__)
app.secret_key = 'heart_disease_severity_predictor_key'

# Improved API URL
API_URL = 'http://127.0.0.1:5000'

@app.route('/')
def index():
    """Improved prediction interface."""
    return render_template('improved_index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle improved prediction request with severity levels."""
    try:
        # Get form data
        patient_data = {
            'age': int(request.form['age']),
            'sex': int(request.form['sex']),
            'cp': int(request.form['cp']),
            'trestbps': int(request.form['trestbps']),
            'chol': int(request.form['chol']),
            'fbs': int(request.form['fbs']),
            'restecg': int(request.form['restecg']),
            'thalch': int(request.form['thalch']),
            'exang': int(request.form['exang']),
            'oldpeak': float(request.form['oldpeak']),
            'slope': int(request.form['slope']),
            'ca': int(request.form['ca']),
            'thal': int(request.form['thal'])
        }

        # Make API request
        response = requests.post(f'{API_URL}/predict', json=patient_data)

        if response.status_code == 200:
            result = response.json()
            return render_template('improved_result.html',
                                 patient_data=patient_data,
                                 result=result)
        else:
            flash('Error making prediction. Please try again.', 'error')
            return redirect(url_for('index'))

    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/api/health')
def health():
    """Check API health."""
    try:
        response = requests.get(f'{API_URL}/health')
        return response.json()
    except:
        return {'status': 'API unavailable'}, 503

if __name__ == '__main__':
    print(" Starting Improved Heart Disease Severity Predictor Web Interface...")
    print(" Features: Binary + Severity Level Prediction")
    print(" Access at: http://127.0.0.1:5001")
    app.run(host='127.0.0.1', port=5001, debug=True)
