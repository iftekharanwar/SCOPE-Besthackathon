import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import os

output_dir = Path('analysis/ml/visualizations')
output_dir.mkdir(exist_ok=True, parents=True)

dataset_path = 'analysis/data/2025+-+BEST+Hackathon+-+dataset.xlsx'
print(f"Loading dataset from {dataset_path}")
df = pd.read_excel(dataset_path)

print('Dataset shape:', df.shape)
print('\nColumns:', df.columns.tolist())
print('\nSample data:')
print(df.head())
print('\nData types:')
print(df.dtypes)
print('\nMissing values:')
print(df.isnull().sum())
print('\nSummary statistics:')
print(df.describe())

with open(output_dir / 'dataset_summary.txt', 'w') as f:
    f.write(f'Dataset shape: {df.shape}\n\n')
    f.write(f'Columns: {df.columns.tolist()}\n\n')
    f.write('Data types:\n')
    f.write(df.dtypes.to_string())
    f.write('\n\nMissing values:\n')
    f.write(df.isnull().sum().to_string())
    f.write('\n\nSummary statistics:\n')
    f.write(df.describe().to_string())

numerical_cols = df.select_dtypes(include=['int64', 'float64']).columns
correlation_matrix = df[numerical_cols].corr()

plt.figure(figsize=(12, 10))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Feature Correlation Matrix')
plt.tight_layout()
plt.savefig(output_dir / 'correlation_matrix.png')
print(f"Saved correlation matrix to {output_dir / 'correlation_matrix.png'}")

key_features = ['POLICYHOLDER_AGE', 'CLAIM_AMOUNT_PAID', 'PREMIUM_AMOUNT_PAID']
for feature in key_features:
    if feature in df.columns:
        plt.figure(figsize=(10, 6))
        sns.histplot(df[feature], kde=True)
        plt.title(f'Distribution of {feature}')
        plt.tight_layout()
        plt.savefig(output_dir / f'{feature.lower()}_distribution.png')
        print(f"Saved {feature} distribution to {output_dir / f'{feature.lower()}_distribution.png'}")

categorical_features = ['WARRANTY', 'CLAIM_REGION', 'VEHICLE_BRAND']
for feature in categorical_features:
    if feature in df.columns:
        plt.figure(figsize=(12, 8))
        value_counts = df[feature].value_counts().sort_values(ascending=False)
        sns.barplot(x=value_counts.index, y=value_counts.values)
        plt.title(f'Distribution of {feature}')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(output_dir / f'{feature.lower()}_distribution.png')
        print(f"Saved {feature} distribution to {output_dir / f'{feature.lower()}_distribution.png'}")


def assign_department(row):
    if row.get('CLAIM_AMOUNT_PAID', 0) > 15000:
        return 'High Value Claims'
    elif 'third-party' in str(row.get('WARRANTY', '')).lower():
        return 'Legal Claims'
    elif row.get('POLICYHOLDER_AGE', 0) > 60 and row.get('CLAIM_AMOUNT_PAID', 0) > 10000:
        return 'Senior Claims'
    elif row.get('PREMIUM_AMOUNT_PAID', 0) > 800:
        return 'VIP Claims'
    elif row.get('CLAIM_REGION') in ['Napoli', 'Naples', 'Caserta']:
        return 'Regional Team - South'
    else:
        return 'Standard Claims'

df['DEPARTMENT'] = df.apply(assign_department, axis=1)

plt.figure(figsize=(12, 8))
dept_counts = df['DEPARTMENT'].value_counts()
sns.barplot(x=dept_counts.index, y=dept_counts.values)
plt.title('Distribution of Assigned Departments')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(output_dir / 'department_distribution.png')
print(f"Saved department distribution to {output_dir / 'department_distribution.png'}")

for feature in key_features:
    if feature in df.columns:
        plt.figure(figsize=(12, 8))
        sns.boxplot(x='DEPARTMENT', y=feature, data=df)
        plt.title(f'Relationship between {feature} and Department')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.savefig(output_dir / f'{feature.lower()}_by_department.png')
        print(f"Saved {feature} by department to {output_dir / f'{feature.lower()}_by_department.png'}")

from sklearn.preprocessing import LabelEncoder

categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
categorical_cols.remove('DEPARTMENT')  # Remove target variable

X = df.copy()
encoders = {}

for col in categorical_cols:
    le = LabelEncoder()
    X[col] = le.fit_transform(X[col].astype(str))
    encoders[col] = le

y = LabelEncoder().fit_transform(df['DEPARTMENT'])

from sklearn.ensemble import RandomForestClassifier

feature_cols = [col for col in X.columns if col != 'DEPARTMENT']
X = X[feature_cols]

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X, y)

feature_importance = pd.DataFrame({
    'Feature': feature_cols,
    'Importance': rf.feature_importances_
}).sort_values('Importance', ascending=False)

plt.figure(figsize=(12, 8))
sns.barplot(x='Importance', y='Feature', data=feature_importance)
plt.title('Feature Importance for Department Assignment')
plt.tight_layout()
plt.savefig(output_dir / 'feature_importance.png')
print(f"Saved feature importance to {output_dir / 'feature_importance.png'}")

feature_importance.to_csv(output_dir / 'feature_importance.csv', index=False)
print(f"Saved feature importance to {output_dir / 'feature_importance.csv'}")

X['DEPARTMENT'] = df['DEPARTMENT']  # Add back the department column
X.to_csv(output_dir / 'processed_dataset.csv', index=False)
print(f"Saved processed dataset to {output_dir / 'processed_dataset.csv'}")

with open(output_dir / 'analysis_report.md', 'w') as f:
    f.write('# Dataset Analysis for ML-Based Claim Routing\n\n')
    
    f.write('## Dataset Overview\n')
    f.write(f'- Total records: {df.shape[0]}\n')
    f.write(f'- Features: {df.shape[1]}\n\n')
    
    f.write('## Key Findings\n\n')
    
    f.write('### Feature Importance\n')
    f.write('The most important features for claim routing are:\n')
    for _, row in feature_importance.head(5).iterrows():
        f.write(f'- {row["Feature"]}: {row["Importance"]:.4f}\n')
    f.write('\n')
    
    f.write('### Department Distribution\n')
    f.write('The distribution of departments based on our simulated rules:\n')
    for dept, count in dept_counts.items():
        f.write(f'- {dept}: {count} claims ({count/len(df)*100:.1f}%)\n')
    f.write('\n')
    
    f.write('### Correlations\n')
    f.write('Significant correlations between features:\n')
    corr_pairs = []
    for i in range(len(numerical_cols)):
        for j in range(i+1, len(numerical_cols)):
            corr = correlation_matrix.iloc[i, j]
            if abs(corr) > 0.3:  # Only report meaningful correlations
                corr_pairs.append((numerical_cols[i], numerical_cols[j], corr))
    
    for col1, col2, corr in sorted(corr_pairs, key=lambda x: abs(x[2]), reverse=True):
        f.write(f'- {col1} and {col2}: {corr:.2f}\n')
    
    f.write('\n## Recommendations for ML Model\n\n')
    f.write('Based on the analysis, we recommend:\n\n')
    f.write('1. Using Random Forest as the primary model due to the mix of categorical and numerical features\n')
    f.write('2. Including all features in the initial model, with special attention to the top 5 important features\n')
    f.write('3. Implementing a hybrid approach that combines ML predictions with business rules for edge cases\n')
    f.write('4. Using stratified sampling during training to handle any class imbalance in department assignments\n')

print(f"Generated analysis report at {output_dir / 'analysis_report.md'}")
print("Dataset analysis complete!")
