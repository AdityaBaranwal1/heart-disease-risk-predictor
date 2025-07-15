"""
Debug the exact input that's failing
"""
import requests
import json

# Exact data from your screenshot
test_data = {
    'age': 67,
    'sex': 1,  # Male
    'cp': 0,   # Asymptomatic
    'trestbps': 158,  # Blood pressure from screenshot
    'chol': 286,
    'fbs': 0,  # False
    'restecg': 0,  # Normal (0, not 1)
    'thalach': 108,  # Fixed spelling
    'exang': 0,  # No (0, not 1) 
    'oldpeak': 1.50,
    'slope': 1,  # Flat
    'ca': 3,
    'thal': 0   # Normal
}

print("Testing exact data from screenshot:")
print("=" * 50)
print(f"Data: {test_data}")

try:
    # Test the API
    response = requests.post("http://localhost:5000/predict", 
                           json=test_data, 
                           timeout=10)
    
    print(f"\nAPI Response Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        result = response.json()
        print("\n✅ SUCCESS!")
        print(json.dumps(result, indent=2))
    else:
        print(f"\n❌ ERROR: {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("\n❌ Cannot connect to API at localhost:5000")
    print("Make sure the API server is running!")
except Exception as e:
    print(f"\n❌ Error: {e}")
