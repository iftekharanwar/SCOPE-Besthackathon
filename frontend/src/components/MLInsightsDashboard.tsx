import { useState } from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';

interface MLInsightsDashboardProps {
  className?: string;
}

export function MLInsightsDashboard({ className }: MLInsightsDashboardProps) {
  const [activeCategory, setActiveCategory] = useState<'feature-importance' | 'model-performance' | 'distributions' | 'time-based' | 'geographic' | 'advanced-analytics'>('feature-importance');

  const visualizations = {
    featureImportance: [
      { 
        title: 'Feature Importance', 
        description: 'The most influential features for the ML model\'s routing decisions',
        image: '/ml-visualizations/feature_importance.png',
        explanation: 'This chart shows that claim amount is the most important feature for routing decisions, followed by premium amount and policyholder age. The model heavily weighs these factors when determining which department should handle a claim. High claim amounts often indicate complex cases requiring specialized teams, while premium amounts help identify VIP customers.'
      },
      { 
        title: 'Correlation Matrix', 
        description: 'Relationships between different claim features',
        image: '/ml-visualizations/correlation_matrix.png',
        explanation: 'The correlation matrix reveals important relationships between claim features. Notice the strong positive correlation between premium amount and claim amount, suggesting that customers with higher premiums tend to file larger claims. Vehicle brand also correlates with claim amount, as luxury vehicles typically have more expensive repairs.'
      }
    ],
    modelPerformance: [
      { 
        title: 'Model Comparison', 
        description: 'Performance comparison of different ML models',
        image: '/ml-visualizations/model_comparison.png',
        explanation: 'This comparison shows that all three models (Random Forest, Gradient Boosting, and Logistic Regression) perform exceptionally well, with accuracy scores above 99%. Random Forest was selected as our primary model due to its perfect accuracy and robust performance across all department types. This high accuracy means claims are consistently routed to the correct departments.'
      },
      { 
        title: 'Random Forest Confusion Matrix', 
        description: 'Accuracy of the Random Forest model by department',
        image: '/ml-visualizations/random_forest_confusion_matrix.png',
        explanation: 'The confusion matrix for our Random Forest model shows perfect classification across all departments. Each number on the diagonal represents correctly classified claims, while zeros elsewhere indicate no misclassifications. This demonstrates that the model can reliably distinguish between different claim types and route them to the appropriate departments.'
      },
      { 
        title: 'Gradient Boosting Confusion Matrix', 
        description: 'Accuracy of the Gradient Boosting model by department',
        image: '/ml-visualizations/gradient_boosting_confusion_matrix.png',
        explanation: 'Similar to Random Forest, the Gradient Boosting model achieves excellent classification results. The diagonal pattern shows correct classifications, with minimal errors. This model could serve as a reliable backup to our primary Random Forest model, offering similar performance characteristics.'
      },
      { 
        title: 'Logistic Regression Confusion Matrix', 
        description: 'Accuracy of the Logistic Regression model by department',
        image: '/ml-visualizations/logistic_regression_confusion_matrix.png',
        explanation: 'Despite being a simpler model, Logistic Regression still achieves high accuracy. The few off-diagonal numbers represent misclassifications, particularly between similar department types. This demonstrates that even a basic model can capture most of the patterns in our insurance claim data, though not as perfectly as the tree-based models.'
      }
    ],
    distributions: [
      { 
        title: 'Department Distribution', 
        description: 'Distribution of claims across departments',
        image: '/ml-visualizations/department_distribution.png',
        explanation: 'This chart shows how claims are distributed across different departments. Standard Claims handles the majority of cases, while specialized departments like High Value Claims and Legal Claims handle fewer but more complex cases. This distribution helps us understand department workloads and resource allocation needs.'
      },
      { 
        title: 'Claim Amount Distribution', 
        description: 'Distribution of claim amounts',
        image: '/ml-visualizations/claim_amount_paid_distribution.png',
        explanation: 'The claim amount distribution reveals that most claims fall in the lower range (below €5,000), with a long tail of higher-value claims. This pattern is typical in insurance data and explains why we need specialized High Value Claims teams to handle the less frequent but more complex expensive claims.'
      },
      { 
        title: 'Premium Amount Distribution', 
        description: 'Distribution of premium amounts',
        image: '/ml-visualizations/premium_amount_paid_distribution.png',
        explanation: 'Premium amounts follow a similar pattern to claim amounts, with most customers paying standard premiums and fewer paying higher amounts. The system uses premium thresholds to identify VIP customers who should receive priority handling, typically those paying above €400 annually.'
      },
      { 
        title: 'Vehicle Brand Distribution', 
        description: 'Distribution of vehicle brands',
        image: '/ml-visualizations/vehicle_brand_distribution.png',
        explanation: 'This chart shows the frequency of different vehicle brands in our claims data. Common brands like Fiat and Renault appear most frequently, while luxury brands like BMW and Mercedes are less common but often associated with higher claim amounts. The model uses vehicle brand as a factor in determining claim complexity and appropriate routing.'
      },
      { 
        title: 'Warranty Distribution', 
        description: 'Distribution of warranty types',
        image: '/ml-visualizations/warranty_distribution.png',
        explanation: 'The warranty type distribution shows that Basic and Comprehensive warranties are most common, while Third-party liability claims occur less frequently. Third-party claims often involve legal considerations and are typically routed to specialized Legal Claims teams regardless of other factors.'
      }
    ],
    timeBased: [
      {
        title: 'Monthly Claim Patterns',
        description: 'How claim volumes vary throughout the year',
        image: '/ml-visualizations/monthly_claim_patterns.png',
        explanation: 'This visualization shows how claim volumes fluctuate by month across different years. Identifying seasonal patterns helps in resource planning and staffing. Peak claim periods may require additional adjusters or specialized teams to handle the increased workload efficiently.'
      },
      {
        title: 'Quarterly Claim Patterns',
        description: 'Seasonal trends in claim volumes',
        image: '/ml-visualizations/quarterly_claim_patterns.png',
        explanation: 'The quarterly view provides a broader perspective on seasonal trends. It helps in quarterly business planning and resource allocation. Consistent patterns across years can inform strategic decisions about staffing and department capacity.'
      },
      {
        title: 'Day of Week Analysis',
        description: 'Claim volumes by day of the week',
        image: '/ml-visualizations/day_of_week_claims.png',
        explanation: 'This visualization reveals which days of the week see the highest claim volumes. This information is crucial for staffing decisions and workload management. Higher claim volumes on specific days may require additional resources to maintain service levels.'
      },
      {
        title: 'Average Claim Amount by Month',
        description: 'Monthly variation in average claim amounts',
        image: '/ml-visualizations/monthly_avg_claim_amount.png',
        explanation: 'This chart shows how the average claim amount varies by month. It helps identify periods when more complex or expensive claims are filed. This information can guide financial planning and reserves management throughout the year.'
      },
      {
        title: 'Claim Volume Heatmap',
        description: 'Detailed view of claim volumes by day and month',
        image: '/ml-visualizations/claim_volume_heatmap.png',
        explanation: 'The heatmap provides a detailed view of claim volumes by day and month. It helps identify specific dates or periods with unusually high claim volumes. This can be useful for identifying external factors affecting claim patterns, such as holidays or weather events.'
      }
    ],
    geographic: [
      {
        title: 'Claim Density by Region',
        description: 'Number of claims filed in each region',
        image: '/ml-visualizations/claim_density_by_region.png',
        explanation: 'This visualization shows the number of claims filed in each region. Regions with higher claim volumes may require dedicated teams or additional resources. This information helps in strategic resource allocation and regional office planning.'
      },
      {
        title: 'Average Claim Amount by Region',
        description: 'Regional variation in claim amounts',
        image: '/ml-visualizations/avg_claim_amount_by_region.png',
        explanation: 'This chart displays the average claim amount for each region. Regions with higher average claim amounts may indicate more complex claims or higher-value insured assets. This information can guide pricing strategies and risk assessment by region.'
      },
      {
        title: 'Risk Score by Region',
        description: 'Composite risk metric by region',
        image: '/ml-visualizations/risk_score_by_region.png',
        explanation: 'The risk score is a composite metric calculated from claim frequency, average amount, variability, and maximum claim amount. Regions with higher risk scores may require more careful underwriting and claim investigation. This metric helps identify geographic areas with potentially higher insurance risk.'
      },
      {
        title: 'Fraud Probability by Region',
        description: 'Estimated fraud risk by region',
        image: '/ml-visualizations/fraud_probability_by_region.png',
        explanation: 'This visualization shows the estimated fraud probability for each region based on various risk factors. Regions with higher fraud probability scores may require enhanced fraud detection measures and more thorough claim investigations. This information helps focus fraud prevention resources where they are most needed.'
      },
      {
        title: 'Region-Department Assignment',
        description: 'How claims from different regions are routed',
        image: '/ml-visualizations/region_department_heatmap.png',
        explanation: 'This heatmap shows how claims from different regions are distributed across departments. It helps identify patterns in claim routing and potential regional specialization needs. For example, some regions may have a higher proportion of claims routed to specialized departments like Legal Claims or High Value Claims.'
      }
    ],
    advancedAnalytics: [
      {
        title: 'Customer Value Segmentation',
        description: 'Segmentation based on premium amounts',
        image: '/ml-visualizations/customer_value_segmentation.png',
        explanation: 'This visualization segments customers based on their premium amounts. Higher premium customers are considered more valuable and may receive priority service. This segmentation helps in customer relationship management and service prioritization.'
      },
      {
        title: 'Risk Score Distribution',
        description: 'Distribution of claims across risk categories',
        image: '/ml-visualizations/risk_score_distribution.png',
        explanation: 'The risk score is calculated based on policyholder age, claim amount, and premium amount. This distribution shows how claims are distributed across different risk categories. Higher risk claims may require more thorough investigation and specialized handling.'
      },
      {
        title: 'Department Workload Forecast',
        description: 'Department workload trends over time',
        image: '/ml-visualizations/department_workload_forecast.png',
        explanation: 'This time series visualization shows how department workloads have changed over time. It can help predict future workloads and plan resource allocation accordingly. Seasonal patterns and trends can inform staffing and capacity planning.'
      },
      {
        title: 'Claim vs Premium Analysis',
        description: 'Relationship between premium and claim amounts',
        image: '/ml-visualizations/claim_vs_premium_scatter.png',
        explanation: 'This scatter plot shows the relationship between premium amounts and claim amounts. It helps identify potential pricing issues and assess the profitability of different customer segments. The coloring by department shows how different types of claims are distributed across this relationship.'
      },
      {
        title: 'Age Group Analysis',
        description: 'Department assignment by age group',
        image: '/ml-visualizations/age_group_analysis.png',
        explanation: 'This visualization shows how claims from different age groups are distributed across departments. It helps identify age-related patterns in claim types and complexity. This information can guide age-specific product development and marketing strategies.'
      },
      {
        title: 'Vehicle Brand Analysis',
        description: 'Claim amount distribution by vehicle brand',
        image: '/ml-visualizations/vehicle_brand_claim_analysis.png',
        explanation: 'This box plot shows the distribution of claim amounts for different vehicle brands. It helps identify brands associated with higher claim amounts or greater variability. This information can inform underwriting and pricing strategies for different vehicle types.'
      },
      {
        title: 'Warranty Type Impact Analysis',
        description: 'How warranty types affect claim amounts',
        image: '/ml-visualizations/warranty_impact_analysis.png',
        explanation: 'This visualization shows how different warranty types affect claim amounts and routing decisions. Third-party liability warranties typically result in higher claim amounts and are often routed to specialized departments. This information helps in product design and pricing strategy.'
      }
    ]
  };

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle>ML Model Insights</CardTitle>
        <CardDescription>
          Visualizations and insights from the machine learning model used for claim routing
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="flex flex-wrap gap-2 mb-4">
          <Button 
            variant={activeCategory === 'feature-importance' ? 'default' : 'outline'} 
            onClick={() => setActiveCategory('feature-importance')}
          >
            Feature Importance
          </Button>
          <Button 
            variant={activeCategory === 'model-performance' ? 'default' : 'outline'} 
            onClick={() => setActiveCategory('model-performance')}
          >
            Model Performance
          </Button>
          <Button 
            variant={activeCategory === 'distributions' ? 'default' : 'outline'} 
            onClick={() => setActiveCategory('distributions')}
          >
            Data Distributions
          </Button>
          <Button 
            variant={activeCategory === 'time-based' ? 'default' : 'outline'} 
            onClick={() => setActiveCategory('time-based')}
          >
            Time-Based Patterns
          </Button>
          <Button 
            variant={activeCategory === 'geographic' ? 'default' : 'outline'} 
            onClick={() => setActiveCategory('geographic')}
          >
            Geographic Analysis
          </Button>
          <Button 
            variant={activeCategory === 'advanced-analytics' ? 'default' : 'outline'} 
            onClick={() => setActiveCategory('advanced-analytics')}
          >
            Advanced Analytics
          </Button>
        </div>
        
        <div className="space-y-6">
          {activeCategory === 'feature-importance' && (
            <>
              {visualizations.featureImportance.map((viz, index) => (
                <div key={index} className="bg-white p-4 rounded-lg shadow">
                  <h3 className="text-lg font-medium mb-2">{viz.title}</h3>
                  <p className="text-sm text-gray-500 mb-4">{viz.description}</p>
                  <div className="flex justify-center">
                    <img 
                      src={viz.image} 
                      alt={viz.title} 
                      className="max-w-full h-auto rounded-md"
                    />
                  </div>
                  <div className="mt-4 p-3 bg-gray-50 rounded-md border border-gray-100">
                    <h4 className="text-sm font-medium text-gray-700 mb-1">What This Means:</h4>
                    <p className="text-sm text-gray-600">{viz.explanation}</p>
                  </div>
                </div>
              ))}
            </>
          )}
          
          {activeCategory === 'model-performance' && (
            <>
              {visualizations.modelPerformance.map((viz, index) => (
                <div key={index} className="bg-white p-4 rounded-lg shadow">
                  <h3 className="text-lg font-medium mb-2">{viz.title}</h3>
                  <p className="text-sm text-gray-500 mb-4">{viz.description}</p>
                  <div className="flex justify-center">
                    <img 
                      src={viz.image} 
                      alt={viz.title} 
                      className="max-w-full h-auto rounded-md"
                    />
                  </div>
                  <div className="mt-4 p-3 bg-gray-50 rounded-md border border-gray-100">
                    <h4 className="text-sm font-medium text-gray-700 mb-1">What This Means:</h4>
                    <p className="text-sm text-gray-600">{viz.explanation}</p>
                  </div>
                </div>
              ))}
            </>
          )}
          
          {activeCategory === 'distributions' && (
            <>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {visualizations.distributions.map((viz, index) => (
                  <div key={index} className="bg-white p-4 rounded-lg shadow">
                    <h3 className="text-lg font-medium mb-2">{viz.title}</h3>
                    <p className="text-sm text-gray-500 mb-4">{viz.description}</p>
                    <div className="flex justify-center">
                      <img 
                        src={viz.image} 
                        alt={viz.title} 
                        className="max-w-full h-auto rounded-md"
                      />
                    </div>
                    <div className="mt-4 p-3 bg-gray-50 rounded-md border border-gray-100">
                      <h4 className="text-sm font-medium text-gray-700 mb-1">What This Means:</h4>
                      <p className="text-sm text-gray-600">{viz.explanation}</p>
                    </div>
                  </div>
                ))}
              </div>
            </>
          )}
          
          {activeCategory === 'time-based' && (
            <>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {visualizations.timeBased.map((viz, index) => (
                  <div key={index} className="bg-white p-4 rounded-lg shadow">
                    <h3 className="text-lg font-medium mb-2">{viz.title}</h3>
                    <p className="text-sm text-gray-500 mb-4">{viz.description}</p>
                    <div className="flex justify-center">
                      <img 
                        src={viz.image} 
                        alt={viz.title} 
                        className="max-w-full h-auto rounded-md"
                      />
                    </div>
                    <div className="mt-4 p-3 bg-gray-50 rounded-md border border-gray-100">
                      <h4 className="text-sm font-medium text-gray-700 mb-1">What This Means:</h4>
                      <p className="text-sm text-gray-600">{viz.explanation}</p>
                    </div>
                  </div>
                ))}
              </div>
            </>
          )}
          
          {activeCategory === 'geographic' && (
            <>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {visualizations.geographic.map((viz, index) => (
                  <div key={index} className="bg-white p-4 rounded-lg shadow">
                    <h3 className="text-lg font-medium mb-2">{viz.title}</h3>
                    <p className="text-sm text-gray-500 mb-4">{viz.description}</p>
                    <div className="flex justify-center">
                      <img 
                        src={viz.image} 
                        alt={viz.title} 
                        className="max-w-full h-auto rounded-md"
                      />
                    </div>
                    <div className="mt-4 p-3 bg-gray-50 rounded-md border border-gray-100">
                      <h4 className="text-sm font-medium text-gray-700 mb-1">What This Means:</h4>
                      <p className="text-sm text-gray-600">{viz.explanation}</p>
                    </div>
                  </div>
                ))}
              </div>
            </>
          )}
          
          {activeCategory === 'advanced-analytics' && (
            <>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {visualizations.advancedAnalytics.map((viz, index) => (
                  <div key={index} className="bg-white p-4 rounded-lg shadow">
                    <h3 className="text-lg font-medium mb-2">{viz.title}</h3>
                    <p className="text-sm text-gray-500 mb-4">{viz.description}</p>
                    <div className="flex justify-center">
                      <img 
                        src={viz.image} 
                        alt={viz.title} 
                        className="max-w-full h-auto rounded-md"
                      />
                    </div>
                    <div className="mt-4 p-3 bg-gray-50 rounded-md border border-gray-100">
                      <h4 className="text-sm font-medium text-gray-700 mb-1">What This Means:</h4>
                      <p className="text-sm text-gray-600">{viz.explanation}</p>
                    </div>
                  </div>
                ))}
              </div>
            </>
          )}
        </div>
      </CardContent>
      <CardFooter className="flex justify-between">
        <p className="text-sm text-gray-500">
          ML Model: Random Forest Classifier (Accuracy: 100%)
        </p>
        <Button variant="outline" size="sm" onClick={() => window.open('/ml-visualizations/model_training_report.md', '_blank')}>
          View Full ML Report
        </Button>
      </CardFooter>
    </Card>
  );
}
