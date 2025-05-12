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

plt.figure(figsize=(14, 10))
region_counts = df['CLAIM_REGION'].value_counts().reset_index()
region_counts.columns = ['CLAIM_REGION', 'COUNT']

region_counts = region_counts.sort_values('COUNT', ascending=False).head(20)  # Top 20 regions

plt.figure(figsize=(14, 8))
sns.barplot(x='COUNT', y='CLAIM_REGION', data=region_counts)
plt.title('Claim Density by Region (Top 20)', fontsize=16)
plt.xlabel('Number of Claims', fontsize=12)
plt.ylabel('Region', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7, axis='x')
plt.tight_layout()
plt.savefig(output_dir / 'claim_density_by_region.png')
print(f"Saved claim density by region to {output_dir / 'claim_density_by_region.png'}")

plt.figure(figsize=(14, 10))
region_avg_claim = df.groupby('CLAIM_REGION')['CLAIM_AMOUNT_PAID'].mean().reset_index()
region_avg_claim.columns = ['CLAIM_REGION', 'AVG_CLAIM_AMOUNT']

region_avg_claim = region_avg_claim.sort_values('AVG_CLAIM_AMOUNT', ascending=False).head(20)  # Top 20 regions

plt.figure(figsize=(14, 8))
sns.barplot(x='AVG_CLAIM_AMOUNT', y='CLAIM_REGION', data=region_avg_claim)
plt.title('Average Claim Amount by Region (Top 20)', fontsize=16)
plt.xlabel('Average Claim Amount (€)', fontsize=12)
plt.ylabel('Region', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7, axis='x')
plt.tight_layout()
plt.savefig(output_dir / 'avg_claim_amount_by_region.png')
print(f"Saved average claim amount by region to {output_dir / 'avg_claim_amount_by_region.png'}")

region_stats = df.groupby('CLAIM_REGION').agg({
    'CLAIM_ID': 'count',
    'CLAIM_AMOUNT_PAID': ['mean', 'std', 'max']
}).reset_index()

region_stats.columns = ['CLAIM_REGION', 'CLAIM_COUNT', 'AVG_CLAIM_AMOUNT', 'STD_CLAIM_AMOUNT', 'MAX_CLAIM_AMOUNT']

region_stats['NORM_COUNT'] = (region_stats['CLAIM_COUNT'] - region_stats['CLAIM_COUNT'].min()) / (region_stats['CLAIM_COUNT'].max() - region_stats['CLAIM_COUNT'].min())
region_stats['NORM_AVG'] = (region_stats['AVG_CLAIM_AMOUNT'] - region_stats['AVG_CLAIM_AMOUNT'].min()) / (region_stats['AVG_CLAIM_AMOUNT'].max() - region_stats['AVG_CLAIM_AMOUNT'].min())
region_stats['NORM_STD'] = (region_stats['STD_CLAIM_AMOUNT'] - region_stats['STD_CLAIM_AMOUNT'].min()) / (region_stats['STD_CLAIM_AMOUNT'].max() - region_stats['STD_CLAIM_AMOUNT'].min())
region_stats['NORM_MAX'] = (region_stats['MAX_CLAIM_AMOUNT'] - region_stats['MAX_CLAIM_AMOUNT'].min()) / (region_stats['MAX_CLAIM_AMOUNT'].max() - region_stats['MAX_CLAIM_AMOUNT'].min())

region_stats['RISK_SCORE'] = (
    region_stats['NORM_COUNT'] * 0.4 + 
    region_stats['NORM_AVG'] * 0.3 + 
    region_stats['NORM_STD'] * 0.2 + 
    region_stats['NORM_MAX'] * 0.1
)

region_risk = region_stats[['CLAIM_REGION', 'RISK_SCORE']].sort_values('RISK_SCORE', ascending=False).head(20)  # Top 20 regions

plt.figure(figsize=(14, 8))
sns.barplot(x='RISK_SCORE', y='CLAIM_REGION', data=region_risk)
plt.title('Risk Score by Region (Top 20)', fontsize=16)
plt.xlabel('Risk Score (0-1)', fontsize=12)
plt.ylabel('Region', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7, axis='x')
plt.tight_layout()
plt.savefig(output_dir / 'risk_score_by_region.png')
print(f"Saved risk score by region to {output_dir / 'risk_score_by_region.png'}")


df['PREMIUM_CLAIM_RATIO'] = df['PREMIUM_AMOUNT_PAID'] / df['CLAIM_AMOUNT_PAID']

region_fraud = df.groupby('CLAIM_REGION').agg({
    'CLAIM_ID': 'count',
    'PREMIUM_CLAIM_RATIO': ['mean', 'min'],
    'CLAIM_AMOUNT_PAID': ['mean', 'max']
}).reset_index()

region_fraud.columns = ['CLAIM_REGION', 'CLAIM_COUNT', 'AVG_PREMIUM_RATIO', 'MIN_PREMIUM_RATIO', 'AVG_CLAIM_AMOUNT', 'MAX_CLAIM_AMOUNT']

region_fraud['NORM_MIN_RATIO'] = (region_fraud['MIN_PREMIUM_RATIO'] - region_fraud['MIN_PREMIUM_RATIO'].min()) / (region_fraud['MIN_PREMIUM_RATIO'].max() - region_fraud['MIN_PREMIUM_RATIO'].min())
region_fraud['NORM_MAX_CLAIM'] = (region_fraud['MAX_CLAIM_AMOUNT'] - region_fraud['MAX_CLAIM_AMOUNT'].min()) / (region_fraud['MAX_CLAIM_AMOUNT'].max() - region_fraud['MAX_CLAIM_AMOUNT'].min())
region_fraud['NORM_COUNT'] = (region_fraud['CLAIM_COUNT'] - region_fraud['CLAIM_COUNT'].min()) / (region_fraud['CLAIM_COUNT'].max() - region_fraud['CLAIM_COUNT'].min())

region_fraud['FRAUD_PROBABILITY'] = (
    (1 - region_fraud['NORM_MIN_RATIO']) * 0.5 + 
    region_fraud['NORM_MAX_CLAIM'] * 0.3 + 
    (1 - region_fraud['NORM_COUNT']) * 0.2
)

region_fraud_prob = region_fraud[['CLAIM_REGION', 'FRAUD_PROBABILITY']].sort_values('FRAUD_PROBABILITY', ascending=False).head(20)  # Top 20 regions

plt.figure(figsize=(14, 8))
sns.barplot(x='FRAUD_PROBABILITY', y='CLAIM_REGION', data=region_fraud_prob)
plt.title('Fraud Probability by Region (Top 20)', fontsize=16)
plt.xlabel('Fraud Probability (0-1)', fontsize=12)
plt.ylabel('Region', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7, axis='x')
plt.tight_layout()
plt.savefig(output_dir / 'fraud_probability_by_region.png')
print(f"Saved fraud probability by region to {output_dir / 'fraud_probability_by_region.png'}")


def assign_department(row):
    if pd.notna(row.get('CLAIM_AMOUNT_PAID', 0)) and row.get('CLAIM_AMOUNT_PAID', 0) > 15000:
        return 'High Value Claims'
    elif pd.notna(row.get('WARRANTY', '')) and 'third-party' in str(row.get('WARRANTY', '')).lower():
        return 'Legal Claims'
    elif pd.notna(row.get('POLICYHOLDER_AGE', 0)) and pd.notna(row.get('CLAIM_AMOUNT_PAID', 0)) and \
         row.get('POLICYHOLDER_AGE', 0) > 60 and row.get('CLAIM_AMOUNT_PAID', 0) > 10000:
        return 'Senior Claims'
    elif pd.notna(row.get('PREMIUM_AMOUNT_PAID', 0)) and row.get('PREMIUM_AMOUNT_PAID', 0) > 800:
        return 'VIP Claims'
    elif pd.notna(row.get('CLAIM_REGION', '')) and row.get('CLAIM_REGION') in ['Napoli', 'Naples', 'Caserta']:
        return 'Regional Team - South'
    else:
        return 'Standard Claims'

df['DEPARTMENT'] = df.apply(assign_department, axis=1)

region_dept = pd.crosstab(df['CLAIM_REGION'], df['DEPARTMENT'])

top_regions = df['CLAIM_REGION'].value_counts().head(15).index
region_dept_filtered = region_dept.loc[top_regions]

plt.figure(figsize=(16, 12))
sns.heatmap(region_dept_filtered, cmap='YlGnBu', annot=True, fmt='d', cbar_kws={'label': 'Number of Claims'})
plt.title('Region-Department Assignment Heatmap (Top 15 Regions)', fontsize=16)
plt.xlabel('Department', fontsize=12)
plt.ylabel('Region', fontsize=12)
plt.tight_layout()
plt.savefig(output_dir / 'region_department_heatmap.png')
print(f"Saved region-department heatmap to {output_dir / 'region_department_heatmap.png'}")

with open(output_dir / 'geographic_analysis.md', 'w') as f:
    f.write('# Geographic Analysis of Insurance Claims\n\n')
    
    f.write('## Claim Density by Region\n')
    f.write('This visualization shows the number of claims filed in each region. ')
    f.write('Regions with higher claim volumes may require dedicated teams or additional resources. ')
    f.write('This information helps in strategic resource allocation and regional office planning.\n\n')
    
    f.write('## Average Claim Amount by Region\n')
    f.write('This chart displays the average claim amount for each region. ')
    f.write('Regions with higher average claim amounts may indicate more complex claims or higher-value insured assets. ')
    f.write('This information can guide pricing strategies and risk assessment by region.\n\n')
    
    f.write('## Risk Score by Region\n')
    f.write('The risk score is a composite metric calculated from claim frequency, average amount, variability, and maximum claim amount. ')
    f.write('Regions with higher risk scores may require more careful underwriting and claim investigation. ')
    f.write('This metric helps identify geographic areas with potentially higher insurance risk.\n\n')
    
    f.write('## Fraud Probability by Region\n')
    f.write('This visualization shows the estimated fraud probability for each region based on various risk factors. ')
    f.write('Regions with higher fraud probability scores may require enhanced fraud detection measures and more thorough claim investigations. ')
    f.write('This information helps focus fraud prevention resources where they are most needed.\n\n')
    
    f.write('## Region-Department Assignment Heatmap\n')
    f.write('This heatmap shows how claims from different regions are distributed across departments. ')
    f.write('It helps identify patterns in claim routing and potential regional specialization needs. ')
    f.write('For example, some regions may have a higher proportion of claims routed to specialized departments like Legal Claims or High Value Claims.\n\n')

print(f"Created geographic analysis markdown file at {output_dir / 'geographic_analysis.md'}")
print("Geographic visualizations complete!")
