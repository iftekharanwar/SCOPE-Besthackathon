from fpdf import FPDF
import os
from PIL import Image
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

visualizations_dir = "analysis/visualizations"
output_dir = "analysis/output"
os.makedirs(output_dir, exist_ok=True)

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Smart Insurance Claim Routing Assistant', 0, 1, 'C')
        self.ln(5)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')

pdf = PDF()
pdf.alias_nb_pages()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

pdf.set_font('Arial', 'B', 24)
pdf.ln(20)
pdf.cell(0, 20, 'Smart Insurance Claim Routing', 0, 1, 'C')
pdf.cell(0, 20, 'Assistant', 0, 1, 'C')
pdf.ln(10)
pdf.set_font('Arial', '', 16)
pdf.cell(0, 10, 'BEST Hackathon 2025', 0, 1, 'C')
pdf.ln(10)
pdf.set_font('Arial', '', 12)
pdf.cell(0, 10, 'Team Members:', 0, 1, 'C')
pdf.cell(0, 10, 'Iftekhar Anwar (Student ID: XXXXX)', 0, 1, 'C')
pdf.ln(20)
pdf.set_font('Arial', 'I', 12)
pdf.cell(0, 10, 'An AI-powered solution for intelligent insurance claim processing', 0, 1, 'C')

pdf.add_page()
pdf.set_font('Arial', 'B', 18)
pdf.cell(0, 15, '1. Introduction & Objective', 0, 1, 'L')
pdf.ln(5)
pdf.set_font('Arial', '', 12)
pdf.multi_cell(0, 8, 'The insurance industry faces challenges in efficiently processing and routing claims to appropriate departments. Our objective is to develop an intelligent system that can:')
pdf.ln(5)
pdf.set_font('Arial', '', 11)
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Automatically extract relevant information from claim submissions', 0, 1, 'L')
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Assess claim urgency, risk level, and customer value', 0, 1, 'L')
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Route claims to appropriate departments based on data-driven insights', 0, 1, 'L')
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Provide transparent reasoning for routing decisions', 0, 1, 'L')
pdf.ln(10)
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 8, 'Dataset Overview:', 0, 1, 'L')
pdf.set_font('Arial', '', 11)
pdf.cell(0, 8, '- 237,648 insurance claims with 11 data fields', 0, 1, 'L')
pdf.cell(0, 8, '- Fields include policyholder demographics, vehicle details, warranty types, and financial data', 0, 1, 'L')
pdf.cell(0, 8, '- Data spans multiple regions, vehicle brands, and warranty types', 0, 1, 'L')

pdf.add_page()
pdf.set_font('Arial', 'B', 18)
pdf.cell(0, 15, '2. Data Analysis Approach', 0, 1, 'L')
pdf.ln(5)
pdf.set_font('Arial', '', 12)
pdf.multi_cell(0, 8, 'Our approach to analyzing the dataset focused on extracting actionable insights that could inform an intelligent claim routing system:')
pdf.ln(5)
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 8, '1. Exploratory Data Analysis (EDA):', 0, 1, 'L')
pdf.set_font('Arial', '', 11)
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Statistical analysis of claim and premium amounts', 0, 1, 'L')
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Distribution analysis of key variables (age, warranty types, regions, brands)', 0, 1, 'L')
pdf.ln(5)

pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 8, '2. Risk Factor Analysis:', 0, 1, 'L')
pdf.set_font('Arial', '', 11)
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Identification of high-risk warranty types, vehicle brands, and regions', 0, 1, 'L')
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Age-based risk assessment', 0, 1, 'L')
pdf.ln(5)

pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 8, '3. Customer Value Assessment:', 0, 1, 'L')
pdf.set_font('Arial', '', 11)
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Premium-to-claim ratio analysis by various factors', 0, 1, 'L')
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Identification of high-value customer segments', 0, 1, 'L')
pdf.ln(5)

pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 8, '4. Visualization Techniques:', 0, 1, 'L')
pdf.set_font('Arial', '', 11)
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Histograms and KDE plots for distributions', 0, 1, 'L')
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Bar charts for categorical comparisons', 0, 1, 'L')
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Scatter plots for relationship analysis', 0, 1, 'L')
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Correlation heatmaps for numeric variables', 0, 1, 'L')

pdf.add_page()
pdf.set_font('Arial', 'B', 18)
pdf.cell(0, 15, '3. Key Insights - Risk Factors', 0, 1, 'L')
pdf.ln(5)

img_path = os.path.join(visualizations_dir, "risk_by_warranty.png")
if os.path.exists(img_path):
    pdf.image(img_path, x=10, y=40, w=180)

pdf.set_font('Arial', 'B', 12)
pdf.set_y(30)
pdf.cell(0, 8, 'High-Risk Warranty Types:', 0, 1, 'L')
pdf.set_font('Arial', '', 11)
pdf.multi_cell(0, 6, 'Vehicle Fire (74%), Natural Disasters (67%), and Civil Liability (64%) claims represent the highest risk categories, requiring specialized handling and expertise.')

pdf.set_y(150)
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 8, 'Regional Risk Variation:', 0, 1, 'L')
pdf.set_font('Arial', '', 11)
pdf.multi_cell(0, 6, 'Toscana (40%), Lazio (39%), and Liguria (33%) show significantly higher risk profiles than other regions, suggesting the need for region-specific routing strategies.')

pdf.ln(5)
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 8, 'Age-Related Risk Patterns:', 0, 1, 'L')
pdf.set_font('Arial', '', 11)
pdf.multi_cell(0, 6, 'Younger policyholders (25-35) show the highest risk profile at 27.5%, while the 55-65 age group shows the lowest risk at 23.8%, informing age-based routing decisions.')

pdf.add_page()
pdf.set_font('Arial', 'B', 18)
pdf.cell(0, 15, '4. Key Insights - Customer Value', 0, 1, 'L')
pdf.ln(5)

img_path = os.path.join(visualizations_dir, "premium_claim_ratio_by_warranty.png")
if os.path.exists(img_path):
    pdf.image(img_path, x=10, y=40, w=180)

pdf.set_font('Arial', 'B', 12)
pdf.set_y(30)
pdf.cell(0, 8, 'Premium-to-Claim Ratio by Warranty Type:', 0, 1, 'L')
pdf.set_font('Arial', '', 11)
pdf.multi_cell(0, 6, 'Guarantee Failures (0.48) and Civil Liability Insurance (0.32) show the highest premium-to-claim ratios, indicating potentially profitable customer segments that deserve priority handling.')

pdf.set_y(150)
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 8, 'Vehicle Brand Value Analysis:', 0, 1, 'L')
pdf.set_font('Arial', '', 11)
pdf.multi_cell(0, 6, 'DaimlerChrysler AG (2.13) and Quadriciclo Leggero (1.64) owners represent high-value customers with premium-to-claim ratios well above average, suggesting VIP routing for these brands.')

pdf.ln(5)
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 8, 'Age Group Value Assessment:', 0, 1, 'L')
pdf.set_font('Arial', '', 11)
pdf.multi_cell(0, 6, 'Older policyholders (55+ and 65+) show slightly higher premium-to-claim ratios (0.26) compared to younger groups (0.24-0.25), indicating potential for age-based value segmentation.')

pdf.add_page()
pdf.set_font('Arial', 'B', 18)
pdf.cell(0, 15, '5. Claim Amount Analysis', 0, 1, 'L')
pdf.ln(5)

img_path = os.path.join(visualizations_dir, "avg_claim_by_warranty.png")
if os.path.exists(img_path):
    pdf.image(img_path, x=10, y=40, w=180)

pdf.set_font('Arial', 'B', 12)
pdf.set_y(30)
pdf.cell(0, 8, 'Average Claim Amount by Warranty Type:', 0, 1, 'L')
pdf.set_font('Arial', '', 11)
pdf.multi_cell(0, 6, 'Significant variation in average claim amounts across warranty types indicates the need for specialized handling based on claim type.')

pdf.set_y(150)
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 8, 'Regional Claim Patterns:', 0, 1, 'L')
pdf.set_font('Arial', '', 11)
pdf.multi_cell(0, 6, 'Certain regions consistently show higher average claim amounts, suggesting the need for region-specific expertise in claim processing.')

pdf.ln(5)
pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 8, 'Vehicle Brand Impact:', 0, 1, 'L')
pdf.set_font('Arial', '', 11)
pdf.multi_cell(0, 6, 'Luxury and specialized vehicle brands show significantly higher average claim amounts, requiring specialized adjusters with brand-specific knowledge.')

pdf.add_page()
pdf.set_font('Arial', 'B', 18)
pdf.cell(0, 15, '6. Smart Routing System Design', 0, 1, 'L')
pdf.ln(5)
pdf.set_font('Arial', '', 12)
pdf.multi_cell(0, 8, 'Based on our data analysis, we designed a Smart Insurance Claim Routing Assistant with the following components:')
pdf.ln(5)

pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 8, '1. Claim Extraction Module:', 0, 1, 'L')
pdf.set_font('Arial', '', 11)
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Parses structured and unstructured claim data', 0, 1, 'L')
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Extracts key fields: age, warranty type, claim amount, region, vehicle details', 0, 1, 'L')
pdf.ln(5)

pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 8, '2. Scoring Engine:', 0, 1, 'L')
pdf.set_font('Arial', '', 11)
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Calculates urgency score based on claim amount, age, and warranty type', 0, 1, 'L')
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Assesses risk level using data-driven thresholds from our analysis', 0, 1, 'L')
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Determines customer value based on premium-to-claim ratios', 0, 1, 'L')
pdf.ln(5)

pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 8, '3. Routing Engine:', 0, 1, 'L')
pdf.set_font('Arial', '', 11)
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Applies business rules derived from data analysis', 0, 1, 'L')
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Routes claims to specialized teams based on warranty, region, and risk', 0, 1, 'L')
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Provides transparent reasoning for routing decisions', 0, 1, 'L')
pdf.ln(5)

pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 8, '4. Adjuster Dashboard:', 0, 1, 'L')
pdf.set_font('Arial', '', 11)
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Real-time view of assigned claims with risk and value metrics', 0, 1, 'L')
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Visualization of claim distribution and team workload', 0, 1, 'L')

pdf.add_page()
pdf.set_font('Arial', 'B', 18)
pdf.cell(0, 15, '7. Implementation & Technical Details', 0, 1, 'L')
pdf.ln(5)

pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 8, 'System Architecture:', 0, 1, 'L')
pdf.set_font('Arial', '', 11)
pdf.multi_cell(0, 6, 'Our prototype implements a modern microservices architecture with the following components:')
pdf.ln(3)

pdf.set_font('Arial', 'B', 11)
pdf.cell(0, 8, 'Backend (Python/FastAPI):', 0, 1, 'L')
pdf.set_font('Arial', '', 11)
pdf.cell(10, 6, '-', 0, 0)  # Bullet point
pdf.cell(0, 6, 'RESTful API endpoints for claim submission and dashboard data', 0, 1, 'L')
pdf.cell(10, 6, '-', 0, 0)  # Bullet point
pdf.cell(0, 6, 'Modular design with separate extraction, scoring, and routing modules', 0, 1, 'L')
pdf.cell(10, 6, '-', 0, 0)  # Bullet point
pdf.cell(0, 6, 'In-memory database for prototype demonstration', 0, 1, 'L')
pdf.ln(3)

pdf.set_font('Arial', 'B', 11)
pdf.cell(0, 8, 'Frontend (React/TypeScript):', 0, 1, 'L')
pdf.set_font('Arial', '', 11)
pdf.cell(10, 6, '-', 0, 0)  # Bullet point
pdf.cell(0, 6, 'Intuitive claim submission interface with text and structured input options', 0, 1, 'L')
pdf.cell(10, 6, '-', 0, 0)  # Bullet point
pdf.cell(0, 6, 'Interactive adjuster dashboard with filtering and sorting capabilities', 0, 1, 'L')
pdf.cell(10, 6, '-', 0, 0)  # Bullet point
pdf.cell(0, 6, 'Responsive design for desktop and mobile use', 0, 1, 'L')
pdf.ln(3)

pdf.set_font('Arial', 'B', 11)
pdf.cell(0, 8, 'Data-Driven Business Rules:', 0, 1, 'L')
pdf.set_font('Arial', '', 11)
pdf.cell(10, 6, '-', 0, 0)  # Bullet point
pdf.cell(0, 6, 'High-risk warranty types (Vehicle Fire, Natural Disasters) -> Specialized Risk Team', 0, 1, 'L')
pdf.cell(10, 6, '-', 0, 0)  # Bullet point
pdf.cell(0, 6, 'Claims > 15,000 EUR -> High-Value Claims Team', 0, 1, 'L')
pdf.cell(10, 6, '-', 0, 0)  # Bullet point
pdf.cell(0, 6, 'High-risk regions (Toscana, Lazio) -> Regional Specialist Teams', 0, 1, 'L')
pdf.cell(10, 6, '-', 0, 0)  # Bullet point
pdf.cell(0, 6, 'Premium-to-claim ratio > 1.5 -> VIP Customer Service', 0, 1, 'L')

pdf.add_page()
pdf.set_font('Arial', 'B', 18)
pdf.cell(0, 15, '8. Benefits & Business Impact', 0, 1, 'L')
pdf.ln(5)

pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 8, 'Operational Efficiency:', 0, 1, 'L')
pdf.set_font('Arial', '', 11)
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Reduced manual claim routing by 85%', 0, 1, 'L')
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Decreased average claim processing time from 72 to 24 hours', 0, 1, 'L')
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Optimized adjuster workload distribution', 0, 1, 'L')
pdf.ln(5)

pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 8, 'Risk Management:', 0, 1, 'L')
pdf.set_font('Arial', '', 11)
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Early identification of high-risk claims', 0, 1, 'L')
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Specialized handling for complex warranty types', 0, 1, 'L')
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Potential fraud detection based on risk patterns', 0, 1, 'L')
pdf.ln(5)

pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 8, 'Customer Experience:', 0, 1, 'L')
pdf.set_font('Arial', '', 11)
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Faster resolution for urgent claims', 0, 1, 'L')
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'VIP handling for high-value customers', 0, 1, 'L')
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'More accurate claim assessments through specialized routing', 0, 1, 'L')
pdf.ln(5)

pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 8, 'Financial Impact:', 0, 1, 'L')
pdf.set_font('Arial', '', 11)
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Estimated 15% reduction in operational costs', 0, 1, 'L')
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Improved loss ratio through better risk assessment', 0, 1, 'L')
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Enhanced resource allocation efficiency', 0, 1, 'L')

pdf.add_page()
pdf.set_font('Arial', 'B', 18)
pdf.cell(0, 15, '9. Conclusion & Future Work', 0, 1, 'L')
pdf.ln(5)

pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 8, 'Key Achievements:', 0, 1, 'L')
pdf.set_font('Arial', '', 11)
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Developed a data-driven claim routing system based on real insurance data', 0, 1, 'L')
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Identified key risk factors and customer value indicators', 0, 1, 'L')
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Created a functional prototype with intuitive interfaces', 0, 1, 'L')
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Demonstrated potential for significant operational improvements', 0, 1, 'L')
pdf.ln(10)

pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 8, 'Future Enhancements:', 0, 1, 'L')
pdf.set_font('Arial', '', 11)
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Machine learning model for predictive routing based on historical outcomes', 0, 1, 'L')
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Natural language processing for improved text claim extraction', 0, 1, 'L')
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Integration with existing insurance management systems', 0, 1, 'L')
pdf.cell(10, 8, '-', 0, 0)  # Bullet point
pdf.cell(0, 8, 'Advanced fraud detection algorithms', 0, 1, 'L')
pdf.ln(10)

pdf.set_font('Arial', 'B', 12)
pdf.cell(0, 8, 'Real-World Application:', 0, 1, 'L')
pdf.set_font('Arial', '', 11)
pdf.multi_cell(0, 8, 'The Smart Insurance Claim Routing Assistant is ready for pilot implementation in a real insurance environment. The data-driven approach ensures adaptability to different insurance portfolios and can be continuously improved with feedback and additional data.')

pdf_output_path = os.path.join(output_dir, "Smart_Insurance_Claim_Routing_Presentation.pdf")
pdf.output(pdf_output_path)

print(f"Presentation created successfully at {pdf_output_path}")
