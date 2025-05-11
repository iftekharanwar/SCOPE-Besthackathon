import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import os
import joblib

output_dir = Path('analysis/ml/models')
output_dir.mkdir(exist_ok=True, parents=True)

dataset_path = 'analysis/ml/visualizations/processed_dataset.csv'
print(f"Loading processed dataset from {dataset_path}")
df = pd.read_csv(dataset_path)

print(f"Dataset shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")

X = df.drop(['CLAIM_ID', 'DEPARTMENT'], axis=1)
y = df['DEPARTMENT']

print(f"Features: {X.columns.tolist()}")
print(f"Target classes: {y.unique().tolist()}")
print(f"Class distribution:\n{y.value_counts()}")

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Training set size: {X_train.shape[0]}")
print(f"Testing set size: {X_test.shape[0]}")

from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import cross_val_score

models = {
    'random_forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'gradient_boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
    'logistic_regression': LogisticRegression(max_iter=1000, random_state=42, multi_class='multinomial')
}

results = {}
for name, model in models.items():
    print(f"\nTraining {name}...")
    
    cv_scores = cross_val_score(model, X_train, y_train, cv=5)
    print(f"Cross-validation scores: {cv_scores}")
    print(f"Mean CV score: {cv_scores.mean():.4f}")
    
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Test accuracy: {accuracy:.4f}")
    
    results[name] = {
        'model': model,
        'cv_scores': cv_scores,
        'mean_cv_score': cv_scores.mean(),
        'test_accuracy': accuracy,
        'y_pred': y_pred
    }
    
    report = classification_report(y_test, y_pred)
    print(f"Classification report:\n{report}")
    
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=y.unique(), yticklabels=y.unique())
    plt.title(f'Confusion Matrix - {name}')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig(output_dir / f'{name}_confusion_matrix.png')
    
    joblib.dump(model, output_dir / f'{name}_model.joblib')
    print(f"Model saved to {output_dir / f'{name}_model.joblib'}")

model_names = list(results.keys())
cv_scores = [results[name]['mean_cv_score'] for name in model_names]
test_scores = [results[name]['test_accuracy'] for name in model_names]

plt.figure(figsize=(10, 6))
x = np.arange(len(model_names))
width = 0.35
plt.bar(x - width/2, cv_scores, width, label='Cross-Validation')
plt.bar(x + width/2, test_scores, width, label='Test')
plt.xlabel('Model')
plt.ylabel('Accuracy')
plt.title('Model Performance Comparison')
plt.xticks(x, model_names)
plt.legend()
plt.tight_layout()
plt.savefig(output_dir / 'model_comparison.png')
print(f"Model comparison saved to {output_dir / 'model_comparison.png'}")

best_model_name = max(results, key=lambda x: results[x]['test_accuracy'])
best_model = results[best_model_name]['model']
best_accuracy = results[best_model_name]['test_accuracy']
print(f"\nBest model: {best_model_name}")
print(f"Best model accuracy: {best_accuracy:.4f}")

joblib.dump(best_model, output_dir / 'best_model.joblib')
print(f"Best model saved to {output_dir / 'best_model.joblib'}")

if hasattr(best_model, 'feature_importances_'):
    feature_importance = pd.DataFrame({
        'Feature': X.columns,
        'Importance': best_model.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    plt.figure(figsize=(12, 8))
    sns.barplot(x='Importance', y='Feature', data=feature_importance.head(15))
    plt.title(f'Feature Importance - {best_model_name}')
    plt.tight_layout()
    plt.savefig(output_dir / 'best_model_feature_importance.png')
    print(f"Feature importance saved to {output_dir / 'best_model_feature_importance.png'}")
    
    feature_importance.to_csv(output_dir / 'best_model_feature_importance.csv', index=False)
    print(f"Feature importance saved to {output_dir / 'best_model_feature_importance.csv'}")

with open(output_dir / 'model_training_report.md', 'w') as f:
    f.write('# ML Model Training Report for Claim Routing\n\n')
    
    f.write('## Dataset Overview\n')
    f.write(f'- Total records: {df.shape[0]}\n')
    f.write(f'- Features used: {len(X.columns)}\n')
    f.write(f'- Target classes: {len(y.unique())}\n\n')
    
    f.write('## Model Performance\n\n')
    
    f.write('| Model | Cross-Validation Accuracy | Test Accuracy |\n')
    f.write('| ----- | ------------------------- | ------------- |\n')
    for name in model_names:
        f.write(f"| {name} | {results[name]['mean_cv_score']:.4f} | {results[name]['test_accuracy']:.4f} |\n")
    
    f.write('\n## Best Model\n\n')
    f.write(f'- **Model**: {best_model_name}\n')
    f.write(f'- **Test Accuracy**: {best_accuracy:.4f}\n\n')
    
    if hasattr(best_model, 'feature_importances_'):
        f.write('## Top Features by Importance\n\n')
        for _, row in feature_importance.head(10).iterrows():
            f.write(f"- {row['Feature']}: {row['Importance']:.4f}\n")
    
    f.write('\n## Recommendations\n\n')
    f.write('1. Use the trained model for claim routing in the application\n')
    f.write('2. Implement a hybrid approach that combines ML predictions with business rules for edge cases\n')
    f.write('3. Consider adding a confidence threshold to fall back to rule-based routing when ML confidence is low\n')
    f.write('4. Periodically retrain the model as new data becomes available\n')
    f.write('5. Monitor model performance in production to ensure continued accuracy\n')

print(f"Model training report generated at {output_dir / 'model_training_report.md'}")
print("Model training complete!")
