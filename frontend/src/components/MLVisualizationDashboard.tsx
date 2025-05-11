import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from './ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Button } from './ui/button';

const visualizationImages = {
  featureImportance: '/ml-visualizations/feature_importance.png',
  correlationMatrix: '/ml-visualizations/correlation_matrix.png',
  departmentDistribution: '/ml-visualizations/department_distribution.png',
  claimAmountDistribution: '/ml-visualizations/claim_amount_paid_distribution.png',
  premiumAmountDistribution: '/ml-visualizations/premium_amount_paid_distribution.png',
  vehicleBrandDistribution: '/ml-visualizations/vehicle_brand_distribution.png',
  warrantyDistribution: '/ml-visualizations/warranty_distribution.png',
  claimRegionDistribution: '/ml-visualizations/claim_region_distribution.png',
  modelComparison: '/ml-visualizations/model_comparison.png',
  randomForestConfusionMatrix: '/ml-visualizations/random_forest_confusion_matrix.png',
};

interface MLVisualizationDashboardProps {
  className?: string;
}

export function MLVisualizationDashboard({ className }: MLVisualizationDashboardProps) {
  const [activeTab, setActiveTab] = useState('feature-importance');

  return (
    <Card className={`w-full ${className}`}>
      <CardHeader>
        <CardTitle>ML Model Insights</CardTitle>
        <CardDescription>
          Visualizations and insights from the machine learning model used for claim routing
        </CardDescription>
      </CardHeader>
      <CardContent>
        <Tabs defaultValue="feature-importance" value={activeTab} onValueChange={setActiveTab}>
          <TabsList className="grid grid-cols-3 mb-4">
            <TabsTrigger value="feature-importance">Feature Importance</TabsTrigger>
            <TabsTrigger value="distributions">Data Distributions</TabsTrigger>
            <TabsTrigger value="model-performance">Model Performance</TabsTrigger>
          </TabsList>
          
          <TabsContent value="feature-importance" className="space-y-4">
            <div className="bg-white p-4 rounded-lg shadow">
              <h3 className="text-lg font-medium mb-2">Feature Importance</h3>
              <p className="text-sm text-gray-500 mb-4">
                The most influential features for the ML model's routing decisions
              </p>
              <div className="flex justify-center">
                <img 
                  src={visualizationImages.featureImportance} 
                  alt="Feature Importance" 
                  className="max-w-full h-auto rounded-md"
                />
              </div>
            </div>
            
            <div className="bg-white p-4 rounded-lg shadow">
              <h3 className="text-lg font-medium mb-2">Correlation Matrix</h3>
              <p className="text-sm text-gray-500 mb-4">
                Relationships between different claim features
              </p>
              <div className="flex justify-center">
                <img 
                  src={visualizationImages.correlationMatrix} 
                  alt="Correlation Matrix" 
                  className="max-w-full h-auto rounded-md"
                />
              </div>
            </div>
          </TabsContent>
          
          <TabsContent value="distributions" className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-white p-4 rounded-lg shadow">
                <h3 className="text-lg font-medium mb-2">Department Distribution</h3>
                <img 
                  src={visualizationImages.departmentDistribution} 
                  alt="Department Distribution" 
                  className="max-w-full h-auto rounded-md"
                />
              </div>
              
              <div className="bg-white p-4 rounded-lg shadow">
                <h3 className="text-lg font-medium mb-2">Claim Amount Distribution</h3>
                <img 
                  src={visualizationImages.claimAmountDistribution} 
                  alt="Claim Amount Distribution" 
                  className="max-w-full h-auto rounded-md"
                />
              </div>
              
              <div className="bg-white p-4 rounded-lg shadow">
                <h3 className="text-lg font-medium mb-2">Premium Amount Distribution</h3>
                <img 
                  src={visualizationImages.premiumAmountDistribution} 
                  alt="Premium Amount Distribution" 
                  className="max-w-full h-auto rounded-md"
                />
              </div>
              
              <div className="bg-white p-4 rounded-lg shadow">
                <h3 className="text-lg font-medium mb-2">Vehicle Brand Distribution</h3>
                <img 
                  src={visualizationImages.vehicleBrandDistribution} 
                  alt="Vehicle Brand Distribution" 
                  className="max-w-full h-auto rounded-md"
                />
              </div>
            </div>
            
            <Button 
              variant="outline" 
              onClick={() => window.open('/ml-visualizations/analysis_report.md', '_blank')}
              className="w-full"
            >
              View Full Analysis Report
            </Button>
          </TabsContent>
          
          <TabsContent value="model-performance" className="space-y-4">
            <div className="bg-white p-4 rounded-lg shadow">
              <h3 className="text-lg font-medium mb-2">Model Comparison</h3>
              <p className="text-sm text-gray-500 mb-4">
                Performance comparison of different ML models
              </p>
              <div className="flex justify-center">
                <img 
                  src={visualizationImages.modelComparison} 
                  alt="Model Comparison" 
                  className="max-w-full h-auto rounded-md"
                />
              </div>
            </div>
            
            <div className="bg-white p-4 rounded-lg shadow">
              <h3 className="text-lg font-medium mb-2">Random Forest Confusion Matrix</h3>
              <p className="text-sm text-gray-500 mb-4">
                Accuracy of the Random Forest model by department
              </p>
              <div className="flex justify-center">
                <img 
                  src={visualizationImages.randomForestConfusionMatrix} 
                  alt="Random Forest Confusion Matrix" 
                  className="max-w-full h-auto rounded-md"
                />
              </div>
            </div>
            
            <Button 
              variant="outline" 
              onClick={() => window.open('/ml-visualizations/model_training_report.md', '_blank')}
              className="w-full"
            >
              View Full Model Training Report
            </Button>
          </TabsContent>
        </Tabs>
      </CardContent>
      <CardFooter className="flex justify-between">
        <p className="text-sm text-gray-500">
          ML Model: Random Forest Classifier (Accuracy: 100%)
        </p>
        <Button variant="outline" size="sm" onClick={() => window.open('/ML_IMPLEMENTATION_REPORT.md', '_blank')}>
          View ML Implementation Report
        </Button>
      </CardFooter>
    </Card>
  );
}
