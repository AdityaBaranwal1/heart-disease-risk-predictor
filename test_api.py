"""
Test the API directly to isolate the issue
"""
import requests
import json

# Test data that passed validation
test_data = {
    'age': 67,
    'sex': 1,
    'cp': 0,
    'trestbps': 160,
    'chol': 286,
    'fbs': 0,
    'restecg': 1,
    'thalach': 108,  # Fixed: was 'thalch', now 'thalach'
    'exang': 1,
    'oldpeak': 1.5,
    'slope': 1,
    'ca': 3,
    'thal': 0
}

print("Testing API endpoint...")
print("=" * 50)

try:
    # Test if API is running
    response = requests.get("http://localhost:5000/health", timeout=5)
    print(f"✅ Health check: {response.status_code}")
except Exception as e:
    print(f"❌ Health check failed: {e}")

try:
    # Test prediction endpoint
    response = requests.post("http://localhost:5000/predict", 
                           json=test_data, 
                           timeout=10)
    
    print(f"📡 API Response Status: {response.status_code}")
    print(f"📄 Response Headers: {dict(response.headers)}")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ SUCCESS! API Response:")
        print(json.dumps(result, indent=2))
    else:
        print("❌ ERROR! API Response:")
        print(f"Status: {response.status_code}")
        print(f"Text: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("❌ Connection Error: Cannot connect to API at localhost:5000")
    print("   Make sure the API server is running!")
except Exception as e:
    print(f"❌ Request failed: {e}")

print("\n" + "=" * 50)
print("Next steps:")
print("1. If connection error: Start the API server")
print("2. If 404 error: Check if /predict endpoint exists") 
print("3. If 500 error: Check API logs for model loading issues")
