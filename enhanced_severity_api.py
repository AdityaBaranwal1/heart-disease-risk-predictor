"""
Enhanced Heart Disease Severity Predictor API
Predicts both binary classification and severity levels (0-4)
"""

import os
import numpy as np
import pandas as pd
import joblib
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedHeartDiseasePredictorAPI:
    def __init__(self):
        """Initialize the enhanced predictor with both binary and severity models."""
        self.app = Flask(__name__)
        self.logger = logger
        
        try:
            # Feature names (must match training data)
            self.feature_names = [
                'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
                'restecg', 'thalch', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
            ]
            
            # Severity level descriptions
            self.severity_descriptions = {
                0: "No Heart Disease",
                1: "Mild Heart Disease", 
                2: "Moderate Heart Disease",
                3: "Severe Heart Disease",
                4: "Very Severe Heart Disease"
            }
            
            # Risk level colors for visualization
            self.risk_colors = {
                0: "#28a745",  # Green
                1: "#ffc107",  # Yellow
                2: "#fd7e14",  # Orange
                3: "#dc3545",  # Red
                4: "#6f42c1"   # Purple
            }
            
            # Load or train models
            self._load_or_train_models()
            
            # Setup Flask routes
            self._setup_routes()
            
            self.logger.info("Enhanced Heart Disease Predictor API initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize API: {e}")
            raise

    def _load_or_train_models(self):
        """Load existing models or train new ones."""
        binary_model_path = 'models/enhanced_binary_model.joblib'
        severity_model_path = 'models/enhanced_severity_model.joblib'
        scaler_path = 'models/enhanced_scaler.joblib'
        
        if (os.path.exists(binary_model_path) and 
            os.path.exists(severity_model_path) and 
            os.path.exists(scaler_path)):
            # Load existing models
            self.binary_model = joblib.load(binary_model_path)
            self.severity_model = joblib.load(severity_model_path)
            self.scaler = joblib.load(scaler_path)
            self.logger.info("Loaded existing enhanced models")
        else:
            # Train new models
            self._train_enhanced_models()
            
    def _train_enhanced_models(self):
        """Train both binary and severity prediction models."""
        self.logger.info("Training enhanced models...")
        
        # Load data
        data = pd.read_csv('heart_disease_data.csv')
        
        # Prepare features
        features_to_drop = ['id', 'num', 'dataset']
        X = data.drop(features_to_drop, axis=1)
        
        # Handle categorical variables
        categorical_columns = X.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            if col == 'sex':
                X[col] = (X[col] == 'Male').astype(int)
            elif col in ['fbs', 'exang']:
                X[col] = (X[col] == 'TRUE').astype(int)
            else:
                # Use label encoding for other categorical variables
                from sklearn.preprocessing import LabelEncoder
                le = LabelEncoder()
                X[col] = le.fit_transform(X[col].astype(str))
        
        # Ensure all columns are numeric
        for col in X.columns:
            if X[col].dtype == 'object':
                X[col] = pd.to_numeric(X[col], errors='coerce')
        
        # Fill any NaN values
        X = X.fillna(X.median())
        
        # Reorder columns to match feature names
        X = X[self.feature_names]
        
        # Create targets
        y_binary = (data['num'] > 0).astype(int)  # Binary: 0 = no disease, 1 = disease
        y_severity = data['num']  # Multi-class: 0-4 severity levels
        
        # Split data
        X_train, X_test, y_binary_train, y_binary_test, y_severity_train, y_severity_test = train_test_split(
            X, y_binary, y_severity, test_size=0.2, random_state=42, stratify=y_binary
        )
        
        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train binary classification model
        self.binary_model = RandomForestClassifier(
            n_estimators=200, 
            max_depth=10, 
            min_samples_split=5,
            random_state=42
        )
        self.binary_model.fit(X_train_scaled, y_binary_train)
        
        # Train severity classification model
        self.severity_model = RandomForestClassifier(
            n_estimators=200, 
            max_depth=12, 
            min_samples_split=3,
            random_state=42
        )
        self.severity_model.fit(X_train_scaled, y_severity_train)
        
        # Evaluate models
        binary_pred = self.binary_model.predict(X_test_scaled)
        severity_pred = self.severity_model.predict(X_test_scaled)
        
        binary_accuracy = accuracy_score(y_binary_test, binary_pred)
        severity_accuracy = accuracy_score(y_severity_test, severity_pred)
        
        self.logger.info(f"Binary model accuracy: {binary_accuracy:.4f}")
        self.logger.info(f"Severity model accuracy: {severity_accuracy:.4f}")
        
        # Save models
        os.makedirs('models', exist_ok=True)
        joblib.dump(self.binary_model, 'models/enhanced_binary_model.joblib')
        joblib.dump(self.severity_model, 'models/enhanced_severity_model.joblib')
        joblib.dump(self.scaler, 'models/enhanced_scaler.joblib')
        
        self.logger.info("Enhanced models trained and saved successfully")

    def _setup_routes(self):
        """Setup Flask API routes."""
        
        @self.app.route('/predict', methods=['POST'])
        def predict():
            """Enhanced prediction endpoint with severity levels."""
            try:
                # Get input data
                data = request.get_json()
                
                # Validate input
                if not data:
                    return jsonify({'error': 'No data provided'}), 400
                
                # Extract features in correct order
                features = []
                for feature_name in self.feature_names:
                    if feature_name not in data:
                        return jsonify({'error': f'Missing feature: {feature_name}'}), 400
                    features.append(float(data[feature_name]))
                
                # Convert to numpy array and scale
                features_array = np.array(features).reshape(1, -1)
                features_scaled = self.scaler.transform(features_array)
                
                # Make predictions
                binary_prediction = self.binary_model.predict(features_scaled)[0]
                binary_probability = self.binary_model.predict_proba(features_scaled)[0]
                
                severity_prediction = self.severity_model.predict(features_scaled)[0]
                severity_probabilities = self.severity_model.predict_proba(features_scaled)[0]
                
                # Prepare response
                response = {
                    'timestamp': datetime.now().isoformat(),
                    'binary_prediction': {
                        'has_heart_disease': bool(binary_prediction),
                        'risk_percentage': float(binary_probability[1] * 100),
                        'confidence': float(max(binary_probability))
                    },
                    'severity_prediction': {
                        'severity_level': int(severity_prediction),
                        'severity_description': self.severity_descriptions[severity_prediction],
                        'severity_probabilities': {
                            str(i): float(prob) for i, prob in enumerate(severity_probabilities)
                        },
                        'risk_color': self.risk_colors[severity_prediction]
                    },
                    'detailed_analysis': {
                        'severity_breakdown': {
                            'No Disease (0)': f"{severity_probabilities[0]*100:.1f}%",
                            'Mild (1)': f"{severity_probabilities[1]*100:.1f}%",
                            'Moderate (2)': f"{severity_probabilities[2]*100:.1f}%",
                            'Severe (3)': f"{severity_probabilities[3]*100:.1f}%",
                            'Very Severe (4)': f"{severity_probabilities[4]*100:.1f}%"
                        }
                    },
                    'input_features': data
                }
                
                return jsonify(response)
                
            except Exception as e:
                self.logger.error(f"Prediction error: {e}")
                return jsonify({'error': str(e)}), 500

        @self.app.route('/health', methods=['GET'])
        def health():
            """Health check endpoint."""
            return jsonify({
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'models_loaded': {
                    'binary_model': self.binary_model is not None,
                    'severity_model': self.severity_model is not None,
                    'scaler': self.scaler is not None
                }
            })

        @self.app.route('/model_info', methods=['GET'])
        def model_info():
            """Get model information."""
            return jsonify({
                'feature_names': self.feature_names,
                'severity_levels': self.severity_descriptions,
                'risk_colors': self.risk_colors,
                'prediction_types': ['binary', 'severity']
            })

    def run(self, host='127.0.0.1', port=5000, debug=True):
        """Run the Flask application."""
        self.logger.info(f"Starting Enhanced Heart Disease Predictor API on {host}:{port}")
        self.app.run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    api = EnhancedHeartDiseasePredictorAPI()
    api.run()
