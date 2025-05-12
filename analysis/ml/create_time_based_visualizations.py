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

df['CLAIM_DATE'] = pd.to_datetime(df['CLAIM_DATE'])

df['CLAIM_YEAR'] = df['CLAIM_DATE'].dt.year
df['CLAIM_MONTH'] = df['CLAIM_DATE'].dt.month
df['CLAIM_DAY'] = df['CLAIM_DATE'].dt.day
df['CLAIM_DAYOFWEEK'] = df['CLAIM_DATE'].dt.dayofweek
df['CLAIM_QUARTER'] = df['CLAIM_DATE'].dt.quarter

plt.figure(figsize=(14, 8))
monthly_claims = df.groupby(['CLAIM_YEAR', 'CLAIM_MONTH']).size().reset_index(name='COUNT')
pivot_monthly = monthly_claims.pivot(index='CLAIM_MONTH', columns='CLAIM_YEAR', values='COUNT')
pivot_monthly.plot(kind='line', marker='o')
plt.title('Monthly Claim Patterns by Year', fontsize=16)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Number of Claims', fontsize=12)
plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(title='Year')
plt.tight_layout()
plt.savefig(output_dir / 'monthly_claim_patterns.png')
print(f"Saved monthly claim patterns to {output_dir / 'monthly_claim_patterns.png'}")

plt.figure(figsize=(12, 7))
quarterly_claims = df.groupby(['CLAIM_YEAR', 'CLAIM_QUARTER']).size().reset_index(name='COUNT')
pivot_quarterly = quarterly_claims.pivot(index='CLAIM_QUARTER', columns='CLAIM_YEAR', values='COUNT')
pivot_quarterly.plot(kind='bar')
plt.title('Quarterly Claim Patterns by Year', fontsize=16)
plt.xlabel('Quarter', fontsize=12)
plt.ylabel('Number of Claims', fontsize=12)
plt.xticks(range(4), ['Q1', 'Q2', 'Q3', 'Q4'])
plt.grid(True, linestyle='--', alpha=0.7, axis='y')
plt.legend(title='Year')
plt.tight_layout()
plt.savefig(output_dir / 'quarterly_claim_patterns.png')
print(f"Saved quarterly claim patterns to {output_dir / 'quarterly_claim_patterns.png'}")

plt.figure(figsize=(12, 7))
day_of_week_claims = df.groupby('CLAIM_DAYOFWEEK').size().reset_index(name='COUNT')
sns.barplot(x='CLAIM_DAYOFWEEK', y='COUNT', data=day_of_week_claims)
plt.title('Claims by Day of Week', fontsize=16)
plt.xlabel('Day of Week', fontsize=12)
plt.ylabel('Number of Claims', fontsize=12)
plt.xticks(range(7), ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
plt.grid(True, linestyle='--', alpha=0.7, axis='y')
plt.tight_layout()
plt.savefig(output_dir / 'day_of_week_claims.png')
print(f"Saved day of week claims to {output_dir / 'day_of_week_claims.png'}")

plt.figure(figsize=(14, 8))
monthly_avg_claim = df.groupby(['CLAIM_YEAR', 'CLAIM_MONTH'])['CLAIM_AMOUNT_PAID'].mean().reset_index()
pivot_monthly_avg = monthly_avg_claim.pivot(index='CLAIM_MONTH', columns='CLAIM_YEAR', values='CLAIM_AMOUNT_PAID')
pivot_monthly_avg.plot(kind='line', marker='o')
plt.title('Average Claim Amount by Month', fontsize=16)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Average Claim Amount (€)', fontsize=12)
plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(title='Year')
plt.tight_layout()
plt.savefig(output_dir / 'monthly_avg_claim_amount.png')
print(f"Saved monthly average claim amount to {output_dir / 'monthly_avg_claim_amount.png'}")

plt.figure(figsize=(16, 10))
day_month_counts = df.groupby(['CLAIM_MONTH', 'CLAIM_DAY']).size().unstack(fill_value=0)
sns.heatmap(day_month_counts, cmap='YlGnBu', annot=False, fmt='d', cbar_kws={'label': 'Number of Claims'})
plt.title('Claim Volume Heatmap (Month vs Day)', fontsize=16)
plt.xlabel('Day of Month', fontsize=12)
plt.ylabel('Month', fontsize=12)
plt.yticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
plt.tight_layout()
plt.savefig(output_dir / 'claim_volume_heatmap.png')
print(f"Saved claim volume heatmap to {output_dir / 'claim_volume_heatmap.png'}")

daily_claims = df.groupby(df['CLAIM_DATE'].dt.date).size()
daily_claims.index = pd.DatetimeIndex(daily_claims.index)

daily_claims = daily_claims.resample('D').asfreq(fill_value=0)

plt.figure(figsize=(16, 6))
daily_claims.plot()
plt.title('Daily Claim Volume Over Time', fontsize=16)
plt.xlabel('Date', fontsize=12)
plt.ylabel('Number of Claims', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig(output_dir / 'daily_claim_volume.png')
print(f"Saved daily claim volume to {output_dir / 'daily_claim_volume.png'}")

with open(output_dir / 'time_based_analysis.md', 'w') as f:
    f.write('# Time-Based Analysis of Insurance Claims\n\n')
    
    f.write('## Monthly Claim Patterns\n')
    f.write('The monthly claim patterns visualization shows how claim volumes vary throughout the year. ')
    f.write('This helps identify seasonal trends and plan resource allocation accordingly. ')
    f.write('Peak claim periods may require additional staff or specialized teams.\n\n')
    
    f.write('## Quarterly Claim Patterns\n')
    f.write('The quarterly view provides a broader perspective on seasonal trends. ')
    f.write('It helps in quarterly business planning and resource allocation. ')
    f.write('Consistent patterns across years can inform strategic decisions.\n\n')
    
    f.write('## Day of Week Analysis\n')
    f.write('This visualization reveals which days of the week see the highest claim volumes. ')
    f.write('This information is crucial for staffing decisions and workload management. ')
    f.write('Higher claim volumes on specific days may require additional resources.\n\n')
    
    f.write('## Average Claim Amount by Month\n')
    f.write('This chart shows how the average claim amount varies by month. ')
    f.write('It helps identify periods when more complex or expensive claims are filed. ')
    f.write('This information can guide financial planning and reserves management.\n\n')
    
    f.write('## Claim Volume Heatmap\n')
    f.write('The heatmap provides a detailed view of claim volumes by day and month. ')
    f.write('It helps identify specific dates or periods with unusually high claim volumes. ')
    f.write('This can be useful for identifying external factors affecting claim patterns.\n\n')
    
    f.write('## Daily Claim Volume Over Time\n')
    f.write('This time series shows the daily claim volume over the entire dataset period. ')
    f.write('It helps identify long-term trends, unusual spikes, and potential anomalies. ')
    f.write('This information is valuable for forecasting future claim volumes.\n\n')

print(f"Created time-based analysis markdown file at {output_dir / 'time_based_analysis.md'}")
print("Time-based visualizations complete!")
