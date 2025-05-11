import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import os

output_dir = Path("analysis/visualizations")
output_dir.mkdir(exist_ok=True)

print("Loading dataset...")
df = pd.read_excel("analysis/data/2025+-+BEST+Hackathon+-+dataset.xlsx")

print("\nDataset Overview:")
print(f"Number of records: {len(df)}")
print(f"Number of columns: {len(df.columns)}")
print("\nColumn names:")
print(df.columns.tolist())

print("\nData types and missing values:")
print(df.info())

print("\nBasic statistics:")
print(df.describe())

print("\nMissing values per column:")
print(df.isnull().sum())


plt.figure(figsize=(10, 6))
sns.histplot(df['POLICYHOLDER_AGE'], bins=20, kde=True)
plt.title('Distribution of Policyholder Age')
plt.xlabel('Age')
plt.ylabel('Count')
plt.savefig(output_dir / "age_distribution.png")
plt.close()

plt.figure(figsize=(8, 6))
gender_counts = df['POLICYHOLDER_GENDER'].value_counts()
gender_counts.plot(kind='pie', autopct='%1.1f%%')
plt.title('Distribution of Policyholder Gender')
plt.ylabel('')
plt.savefig(output_dir / "gender_distribution.png")
plt.close()

plt.figure(figsize=(12, 6))
warranty_counts = df['WARRANTY'].value_counts()
warranty_counts.plot(kind='bar')
plt.title('Distribution of Warranty Types')
plt.xlabel('Warranty Type')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(output_dir / "warranty_distribution.png")
plt.close()

plt.figure(figsize=(10, 6))
sns.histplot(df['CLAIM_AMOUNT_PAID'], bins=20, kde=True)
plt.title('Distribution of Claim Amount Paid')
plt.xlabel('Claim Amount')
plt.ylabel('Count')
plt.savefig(output_dir / "claim_amount_distribution.png")
plt.close()

plt.figure(figsize=(10, 6))
sns.histplot(df['PREMIUM_AMOUNT_PAID'], bins=20, kde=True)
plt.title('Distribution of Premium Amount Paid')
plt.xlabel('Premium Amount')
plt.ylabel('Count')
plt.savefig(output_dir / "premium_amount_distribution.png")
plt.close()

plt.figure(figsize=(12, 6))
region_counts = df['CLAIM_REGION'].value_counts().head(10)
region_counts.plot(kind='bar')
plt.title('Top 10 Claim Regions')
plt.xlabel('Region')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(output_dir / "region_distribution.png")
plt.close()

plt.figure(figsize=(12, 6))
brand_counts = df['VEHICLE_BRAND'].value_counts().head(10)
brand_counts.plot(kind='bar')
plt.title('Top 10 Vehicle Brands')
plt.xlabel('Brand')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(output_dir / "brand_distribution.png")
plt.close()

plt.figure(figsize=(10, 6))
sns.scatterplot(x='POLICYHOLDER_AGE', y='CLAIM_AMOUNT_PAID', data=df)
plt.title('Correlation between Policyholder Age and Claim Amount')
plt.xlabel('Age')
plt.ylabel('Claim Amount')
plt.savefig(output_dir / "age_vs_claim_amount.png")
plt.close()

plt.figure(figsize=(10, 6))
sns.scatterplot(x='PREMIUM_AMOUNT_PAID', y='CLAIM_AMOUNT_PAID', data=df)
plt.title('Correlation between Premium Amount and Claim Amount')
plt.xlabel('Premium Amount')
plt.ylabel('Claim Amount')
plt.savefig(output_dir / "premium_vs_claim_amount.png")
plt.close()

plt.figure(figsize=(12, 6))
warranty_avg_claim = df.groupby('WARRANTY')['CLAIM_AMOUNT_PAID'].mean().sort_values(ascending=False)
warranty_avg_claim.plot(kind='bar')
plt.title('Average Claim Amount by Warranty Type')
plt.xlabel('Warranty Type')
plt.ylabel('Average Claim Amount')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(output_dir / "avg_claim_by_warranty.png")
plt.close()

plt.figure(figsize=(12, 6))
brand_avg_claim = df.groupby('VEHICLE_BRAND')['CLAIM_AMOUNT_PAID'].mean().sort_values(ascending=False).head(10)
brand_avg_claim.plot(kind='bar')
plt.title('Average Claim Amount by Top 10 Vehicle Brands')
plt.xlabel('Vehicle Brand')
plt.ylabel('Average Claim Amount')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(output_dir / "avg_claim_by_brand.png")
plt.close()

plt.figure(figsize=(12, 6))
region_avg_claim = df.groupby('CLAIM_REGION')['CLAIM_AMOUNT_PAID'].mean().sort_values(ascending=False).head(10)
region_avg_claim.plot(kind='bar')
plt.title('Average Claim Amount by Top 10 Regions')
plt.xlabel('Region')
plt.ylabel('Average Claim Amount')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(output_dir / "avg_claim_by_region.png")
plt.close()

df['AGE_GROUP'] = pd.cut(df['POLICYHOLDER_AGE'], bins=[0, 25, 35, 45, 55, 65, 100], labels=['<25', '25-35', '35-45', '45-55', '55-65', '65+'])
plt.figure(figsize=(10, 6))
age_group_avg_claim = df.groupby('AGE_GROUP')['CLAIM_AMOUNT_PAID'].mean()
age_group_avg_claim.plot(kind='bar')
plt.title('Average Claim Amount by Age Group')
plt.xlabel('Age Group')
plt.ylabel('Average Claim Amount')
plt.tight_layout()
plt.savefig(output_dir / "avg_claim_by_age_group.png")
plt.close()

plt.figure(figsize=(8, 6))
gender_avg_claim = df.groupby('POLICYHOLDER_GENDER')['CLAIM_AMOUNT_PAID'].mean()
gender_avg_claim.plot(kind='bar')
plt.title('Average Claim Amount by Gender')
plt.xlabel('Gender')
plt.ylabel('Average Claim Amount')
plt.tight_layout()
plt.savefig(output_dir / "avg_claim_by_gender.png")
plt.close()

plt.figure(figsize=(12, 10))
numeric_df = df.select_dtypes(include=[np.number])
correlation = numeric_df.corr()
sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap of Numeric Variables')
plt.tight_layout()
plt.savefig(output_dir / "correlation_heatmap.png")
plt.close()

high_claim_threshold = df['CLAIM_AMOUNT_PAID'].quantile(0.75)
df['HIGH_CLAIM'] = df['CLAIM_AMOUNT_PAID'] > high_claim_threshold

risk_factors = {}

warranty_risk = df.groupby('WARRANTY')['HIGH_CLAIM'].mean().sort_values(ascending=False)
plt.figure(figsize=(12, 6))
warranty_risk.plot(kind='bar')
plt.title('Risk Factor by Warranty Type (Proportion of High Claims)')
plt.xlabel('Warranty Type')
plt.ylabel('Risk Factor')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(output_dir / "risk_by_warranty.png")
plt.close()

brand_risk = df.groupby('VEHICLE_BRAND')['HIGH_CLAIM'].mean().sort_values(ascending=False).head(10)
plt.figure(figsize=(12, 6))
brand_risk.plot(kind='bar')
plt.title('Risk Factor by Top 10 Vehicle Brands (Proportion of High Claims)')
plt.xlabel('Vehicle Brand')
plt.ylabel('Risk Factor')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(output_dir / "risk_by_brand.png")
plt.close()

region_risk = df.groupby('CLAIM_REGION')['HIGH_CLAIM'].mean().sort_values(ascending=False).head(10)
plt.figure(figsize=(12, 6))
region_risk.plot(kind='bar')
plt.title('Risk Factor by Top 10 Regions (Proportion of High Claims)')
plt.xlabel('Region')
plt.ylabel('Risk Factor')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(output_dir / "risk_by_region.png")
plt.close()

age_group_risk = df.groupby('AGE_GROUP')['HIGH_CLAIM'].mean()
plt.figure(figsize=(10, 6))
age_group_risk.plot(kind='bar')
plt.title('Risk Factor by Age Group (Proportion of High Claims)')
plt.xlabel('Age Group')
plt.ylabel('Risk Factor')
plt.tight_layout()
plt.savefig(output_dir / "risk_by_age_group.png")
plt.close()

high_premium_threshold = df['PREMIUM_AMOUNT_PAID'].quantile(0.75)
df['HIGH_PREMIUM'] = df['PREMIUM_AMOUNT_PAID'] > high_premium_threshold

df['PREMIUM_CLAIM_RATIO'] = df['PREMIUM_AMOUNT_PAID'] / df['CLAIM_AMOUNT_PAID']
warranty_ratio = df.groupby('WARRANTY')['PREMIUM_CLAIM_RATIO'].mean().sort_values(ascending=False)
plt.figure(figsize=(12, 6))
warranty_ratio.plot(kind='bar')
plt.title('Premium to Claim Ratio by Warranty Type')
plt.xlabel('Warranty Type')
plt.ylabel('Premium/Claim Ratio')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(output_dir / "premium_claim_ratio_by_warranty.png")
plt.close()

brand_ratio = df.groupby('VEHICLE_BRAND')['PREMIUM_CLAIM_RATIO'].mean().sort_values(ascending=False).head(10)
plt.figure(figsize=(12, 6))
brand_ratio.plot(kind='bar')
plt.title('Premium to Claim Ratio by Top 10 Vehicle Brands')
plt.xlabel('Vehicle Brand')
plt.ylabel('Premium/Claim Ratio')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig(output_dir / "premium_claim_ratio_by_brand.png")
plt.close()

age_group_ratio = df.groupby('AGE_GROUP')['PREMIUM_CLAIM_RATIO'].mean()
plt.figure(figsize=(10, 6))
age_group_ratio.plot(kind='bar')
plt.title('Premium to Claim Ratio by Age Group')
plt.xlabel('Age Group')
plt.ylabel('Premium/Claim Ratio')
plt.tight_layout()
plt.savefig(output_dir / "premium_claim_ratio_by_age_group.png")
plt.close()

with open(output_dir / "key_insights.txt", "w") as f:
    f.write("# Key Insights from Insurance Claims Dataset\n\n")
    
    f.write("## General Statistics\n")
    f.write(f"Total number of claims: {len(df)}\n")
    f.write(f"Average claim amount: {df['CLAIM_AMOUNT_PAID'].mean():.2f}\n")
    f.write(f"Average premium amount: {df['PREMIUM_AMOUNT_PAID'].mean():.2f}\n")
    f.write(f"Average policyholder age: {df['POLICYHOLDER_AGE'].mean():.2f}\n\n")
    
    f.write("## Risk Factors\n")
    f.write("Top 5 high-risk warranty types:\n")
    for warranty, risk in warranty_risk.head(5).items():
        f.write(f"- {warranty}: {risk:.2%}\n")
    
    f.write("\nTop 5 high-risk vehicle brands:\n")
    for brand, risk in brand_risk.head(5).items():
        f.write(f"- {brand}: {risk:.2%}\n")
    
    f.write("\nTop 5 high-risk regions:\n")
    for region, risk in region_risk.head(5).items():
        f.write(f"- {region}: {risk:.2%}\n")
    
    f.write("\nRisk by age group:\n")
    for age_group, risk in age_group_risk.items():
        f.write(f"- {age_group}: {risk:.2%}\n")
    
    f.write("\n## Customer Value Insights\n")
    f.write("Top 5 warranty types by premium/claim ratio:\n")
    for warranty, ratio in warranty_ratio.head(5).items():
        f.write(f"- {warranty}: {ratio:.2f}\n")
    
    f.write("\nTop 5 vehicle brands by premium/claim ratio:\n")
    for brand, ratio in brand_ratio.head(5).items():
        f.write(f"- {brand}: {ratio:.2f}\n")
    
    f.write("\nPremium/claim ratio by age group:\n")
    for age_group, ratio in age_group_ratio.items():
        f.write(f"- {age_group}: {ratio:.2f}\n")

print("\nAnalysis complete. Visualizations and insights saved to", output_dir)
