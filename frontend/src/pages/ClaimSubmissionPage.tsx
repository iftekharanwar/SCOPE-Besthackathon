import React, { useState } from 'react';
import { AlertCircle, Send, FileText, Database } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Textarea } from '../components/ui/textarea';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '../components/ui/card';
import { submitClaim, RoutingDecision } from '../api/claimService';

const ClaimSubmissionPage: React.FC = () => {
  const [claimText, setClaimText] = useState('');
  const [isTextMode, setIsTextMode] = useState(true);
  const [jsonData, setJsonData] = useState('{\n  "POLICYHOLDER_AGE": 45,\n  "WARRANTY": "comprehensive",\n  "CLAIM_AMOUNT_PAID": 8500,\n  "PREMIUM_AMOUNT_PAID": 1200,\n  "CLAIM_REGION": "Rome",\n  "VEHICLE_BRAND": "Audi"\n}');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<RoutingDecision | null>(null);

  const handleSubmit = async () => {
    try {
      setLoading(true);
      setError(null);
      
      let payload;
      if (isTextMode) {
        payload = { text: claimText };
      } else {
        try {
          const structuredData = JSON.parse(jsonData);
          payload = { structured_data: structuredData };
        } catch (e) {
          setError('Invalid JSON format. Please check your input.');
          setLoading(false);
          return;
        }
      }
      
      const response = await submitClaim(payload);
      setResult(response);
    } catch (err) {
      setError('Failed to submit claim. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleModeToggle = (mode: 'text' | 'json') => {
    setIsTextMode(mode === 'text');
    setResult(null);
  };

  const getExampleText = () => {
    setClaimText("I'm a 65-year-old policyholder. I live in Milan. My BMW 5 Series was hit by another vehicle. Claim type: third-party liability. Rear bumper damaged badly. Claim is around €18,000.");
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h2 className="text-3xl font-bold mb-2">Submit Insurance Claim</h2>
        <p className="text-gray-600">
          Enter claim details as text or structured JSON data to route it to the appropriate team.
        </p>
      </div>

      <div className="mb-6">
        <div className="flex space-x-2 mb-4">
          <Button
            variant={isTextMode ? "default" : "outline"}
            onClick={() => handleModeToggle('text')}
            className="flex items-center gap-2"
          >
            <FileText size={16} />
            Text Input
          </Button>
          <Button
            variant={!isTextMode ? "default" : "outline"}
            onClick={() => handleModeToggle('json')}
            className="flex items-center gap-2"
          >
            <Database size={16} />
            JSON Input
          </Button>
        </div>

        {isTextMode ? (
          <Card>
            <CardHeader>
              <CardTitle>Claim Description</CardTitle>
              <CardDescription>
                Describe the claim in natural language, including details like policyholder age, 
                location, vehicle information, and claim amount.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Textarea
                placeholder="Enter claim details here..."
                value={claimText}
                onChange={(e) => setClaimText(e.target.value)}
                rows={6}
                className="w-full"
              />
            </CardContent>
            <CardFooter className="flex justify-between">
              <Button variant="outline" onClick={getExampleText}>
                Load Example
              </Button>
              <Button 
                onClick={handleSubmit} 
                disabled={loading || !claimText.trim()}
                className="flex items-center gap-2"
              >
                <Send size={16} />
                Submit Claim
              </Button>
            </CardFooter>
          </Card>
        ) : (
          <Card>
            <CardHeader>
              <CardTitle>Structured JSON Data</CardTitle>
              <CardDescription>
                Provide claim details in JSON format with fields like POLICYHOLDER_AGE, WARRANTY, 
                CLAIM_AMOUNT_PAID, etc.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <Textarea
                placeholder="Enter JSON data here..."
                value={jsonData}
                onChange={(e) => setJsonData(e.target.value)}
                rows={10}
                className="w-full font-mono text-sm"
              />
            </CardContent>
            <CardFooter className="flex justify-end">
              <Button 
                onClick={handleSubmit} 
                disabled={loading || !jsonData.trim()}
                className="flex items-center gap-2"
              >
                <Send size={16} />
                Submit Claim
              </Button>
            </CardFooter>
          </Card>
        )}
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md mb-6 flex items-start">
          <AlertCircle className="mr-2 h-5 w-5 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {result && (
        <Card className="mb-8 border-blue-200 bg-blue-50">
          <CardHeader>
            <CardTitle className="text-blue-800">Claim Routing Result</CardTitle>
            <CardDescription className="text-blue-600">
              Claim ID: {result.claim_id}
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <h4 className="font-semibold mb-1">Assigned Team</h4>
              <p className="text-lg font-bold text-blue-700">{result.assigned_team}</p>
            </div>
            
            <div className="grid grid-cols-3 gap-4">
              <div>
                <h4 className="font-semibold mb-1">Urgency</h4>
                <div className={`inline-block px-3 py-1 rounded-full text-white font-medium ${
                  result.urgency === 'High' ? 'bg-red-500' : 
                  result.urgency === 'Medium' ? 'bg-yellow-500' : 'bg-green-500'
                }`}>
                  {result.urgency}
                </div>
              </div>
              
              <div>
                <h4 className="font-semibold mb-1">Risk Score</h4>
                <div className="flex items-center">
                  <div className="w-full bg-gray-200 rounded-full h-2.5">
                    <div 
                      className={`h-2.5 rounded-full ${
                        result.risk_score > 0.7 ? 'bg-red-500' : 
                        result.risk_score > 0.4 ? 'bg-yellow-500' : 'bg-green-500'
                      }`} 
                      style={{ width: `${result.risk_score * 100}%` }}
                    ></div>
                  </div>
                  <span className="ml-2 font-medium">{Math.round(result.risk_score * 100)}%</span>
                </div>
              </div>
              
              <div>
                <h4 className="font-semibold mb-1">Customer Value</h4>
                <div className={`inline-block px-3 py-1 rounded-full text-white font-medium ${
                  result.customer_value === 'VIP' ? 'bg-purple-500' : 
                  result.customer_value === 'Premium' ? 'bg-blue-500' : 'bg-gray-500'
                }`}>
                  {result.customer_value}
                </div>
              </div>
            </div>
            
            <div>
              <h4 className="font-semibold mb-2">Routing Reasons</h4>
              <ul className="list-disc pl-5 space-y-1">
                {result.reasoning.map((reason, index) => (
                  <li key={index} className="text-gray-700">{reason}</li>
                ))}
              </ul>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default ClaimSubmissionPage;
