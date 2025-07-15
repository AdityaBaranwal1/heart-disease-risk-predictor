"""
Quick test to identify the validation issue
"""

# Test data from the screenshot
test_data = {
    'age': 67,
    'sex': 1,  # Male
    'cp': 0,   # Asymptomatic  
    'trestbps': 160,
    'chol': 286,
    'fbs': 0,  # False
    'restecg': 1,  # Normal -> should be 0 for normal?
    'thalch': 108,
    'exang': 1,  # Yes
    'oldpeak': 1.5,
    'slope': 1,  # Flat
    'ca': 3,
    'thal': 0   # Normal -> this might be the issue
}

# Expected validation ranges from the API
validations = {
    'age': (0, 120),
    'sex': (0, 1),
    'cp': (0, 3),
    'trestbps': (50, 300),
    'chol': (0, 600),
    'fbs': (0, 1),
    'restecg': (0, 2),
    'thalch': (50, 250),
    'exang': (0, 1),
    'oldpeak': (0, 10),
    'slope': (0, 2),
    'ca': (0, 4),
    'thal': (0, 3)
}

print("Testing validation for screenshot data:")
print("=" * 50)

errors = []
for feature, (min_val, max_val) in validations.items():
    value = test_data[feature]
    if not (min_val <= value <= max_val):
        errors.append(f"{feature} value {value} outside valid range [{min_val}, {max_val}]")
        print(f"❌ {feature}: {value} is outside range [{min_val}, {max_val}]")
    else:
        print(f"✅ {feature}: {value} is valid (range [{min_val}, {max_val}])")

print("\n" + "=" * 50)
if errors:
    print("VALIDATION ERRORS FOUND:")
    for error in errors:
        print(f"  - {error}")
else:
    print("✅ ALL VALIDATIONS PASSED!")

print(f"\nData being sent: {test_data}")
