import { useState } from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';

interface MLInsightsDashboardProps {
  className?: string;
}

export function MLInsightsDashboard({ className }: MLInsightsDashboardProps) {
  const [activeCategory, setActiveCategory] = useState<'feature-importance' | 'model-performance' | 'distributions'>('feature-importance');

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
        <div className="flex gap-2 mb-4">
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
