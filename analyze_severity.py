import pandas as pd
import numpy as np

# Load and analyze the data
data = pd.read_csv('heart_disease_data.csv')

print('Heart Disease Severity Distribution:')
severity_dist = data['num'].value_counts().sort_index()
print(severity_dist)

print(f'\nTotal samples: {len(data)}')
print(f'Binary distribution: No Disease (0): {(data["num"] == 0).sum()}, Disease (1-4): {(data["num"] > 0).sum()}')

# Show percentages
print('\nPercentage distribution:')
for severity in range(5):
    count = (data['num'] == severity).sum()
    percentage = (count / len(data)) * 100
    print(f'Severity {severity}: {count} samples ({percentage:.1f}%)')
