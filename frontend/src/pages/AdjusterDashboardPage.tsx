import React, { useState, useEffect } from 'react';
import { BarChart3, RefreshCw, Filter, AlertTriangle, CheckCircle, XCircle, Brain } from 'lucide-react';
import { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { getAdjusterDashboard, RoutingDecision } from '../api/claimService';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import { MLInsightsDashboard } from '../components/MLInsightsDashboard';

const AdjusterDashboardPage: React.FC = () => {
  const [claims, setClaims] = useState<RoutingDecision[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedTeam, setSelectedTeam] = useState<string | null>(null);
  const [expandedClaim, setExpandedClaim] = useState<string | null>(null);
  const [overrideStatus, setOverrideStatus] = useState<Record<string, 'approved' | 'rejected' | null>>({});

  useEffect(() => {
    fetchClaims();
  }, [selectedTeam]);

  const fetchClaims = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getAdjusterDashboard(selectedTeam || undefined);
      setClaims(data);
    } catch (err) {
      setError('Failed to fetch claims. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleTeamFilter = (team: string | null) => {
    setSelectedTeam(team === selectedTeam ? null : team);
  };

  const toggleClaimExpand = (claimId: string) => {
    setExpandedClaim(expandedClaim === claimId ? null : claimId);
  };

  const handleOverride = (claimId: string, status: 'approved' | 'rejected') => {
    setOverrideStatus({
      ...overrideStatus,
      [claimId]: status
    });
  };

  const teams = Array.from(new Set(claims.map(claim => claim.assigned_team)));

  const urgencyData = [
    { name: 'High', value: claims.filter(c => c.urgency === 'High').length, color: '#ef4444' },
    { name: 'Medium', value: claims.filter(c => c.urgency === 'Medium').length, color: '#f59e0b' },
    { name: 'Low', value: claims.filter(c => c.urgency === 'Low').length, color: '#10b981' },
  ].filter(item => item.value > 0);

  const customerValueData = [
    { name: 'VIP', value: claims.filter(c => c.customer_value === 'VIP').length, color: '#8b5cf6' },
    { name: 'Premium', value: claims.filter(c => c.customer_value === 'Premium').length, color: '#3b82f6' },
    { name: 'Standard', value: claims.filter(c => c.customer_value === 'Standard').length, color: '#6b7280' },
  ].filter(item => item.value > 0);

  const [showMLInsights, setShowMLInsights] = useState(false);

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <div>
          <h2 className="text-3xl font-bold mb-2">Adjuster Dashboard</h2>
          <p className="text-gray-600">
            View and manage assigned insurance claims
          </p>
        </div>
        <div className="flex gap-2">
          <Button 
            onClick={() => setShowMLInsights(!showMLInsights)} 
            variant="secondary" 
            className="flex items-center gap-2"
          >
            <Brain size={16} />
            {showMLInsights ? 'Hide ML Insights' : 'Show ML Insights'}
          </Button>
          <Button onClick={fetchClaims} variant="outline" className="flex items-center gap-2">
            <RefreshCw size={16} />
            Refresh
          </Button>
        </div>
      </div>
      
      {showMLInsights && (
        <div className="mb-8">
          <MLInsightsDashboard />
        </div>
      )}

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md mb-6 flex items-start">
          <AlertTriangle className="mr-2 h-5 w-5 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {loading ? (
        <div className="text-center py-12">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-700 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading claims...</p>
        </div>
      ) : (
        <>
          {claims.length > 0 ? (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <BarChart3 className="h-5 w-5" />
                    Claims Overview
                  </CardTitle>
                  <CardDescription>
                    Total Claims: {claims.length}
                  </CardDescription>
                </CardHeader>
                <CardContent className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={urgencyData}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                        label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                      >
                        {urgencyData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip />
                      <Legend />
                    </PieChart>
                  </ResponsiveContainer>
                </CardContent>
                <CardFooter>
                  <p className="text-sm text-gray-500">Distribution by urgency level</p>
                </CardFooter>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <BarChart3 className="h-5 w-5" />
                    Customer Value
                  </CardTitle>
                  <CardDescription>
                    Distribution by customer value
                  </CardDescription>
                </CardHeader>
                <CardContent className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={customerValueData}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                        label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                      >
                        {customerValueData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip />
                      <Legend />
                    </PieChart>
                  </ResponsiveContainer>
                </CardContent>
                <CardFooter>
                  <p className="text-sm text-gray-500">Distribution by customer value</p>
                </CardFooter>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Filter className="h-5 w-5" />
                    Filter by Team
                  </CardTitle>
                  <CardDescription>
                    Select a team to filter claims
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="flex flex-wrap gap-2">
                    {teams.map(team => (
                      <Badge
                        key={team}
                        variant={selectedTeam === team ? "default" : "outline"}
                        className="cursor-pointer"
                        onClick={() => handleTeamFilter(team)}
                      >
                        {team}
                      </Badge>
                    ))}
                    {selectedTeam && (
                      <Badge
                        variant="secondary"
                        className="cursor-pointer"
                        onClick={() => handleTeamFilter(null)}
                      >
                        Clear Filter
                      </Badge>
                    )}
                  </div>
                </CardContent>
                <CardFooter>
                  <p className="text-sm text-gray-500">
                    {selectedTeam 
                      ? `Showing ${claims.length} claims for ${selectedTeam}`
                      : 'Showing all claims'}
                  </p>
                </CardFooter>
              </Card>
            </div>
          ) : null}

          <div className="space-y-4">
            <h3 className="text-xl font-semibold mb-4">
              {claims.length > 0 
                ? `${claims.length} Claims ${selectedTeam ? `for ${selectedTeam}` : ''}`
                : 'No claims found'}
            </h3>
            
            {claims.map(claim => (
              <Card 
                key={claim.claim_id} 
                className={`border-l-4 ${
                  claim.urgency === 'High' ? 'border-l-red-500' : 
                  claim.urgency === 'Medium' ? 'border-l-yellow-500' : 'border-l-green-500'
                }`}
              >
                <CardHeader className="pb-2">
                  <div className="flex justify-between items-start">
                    <div>
                      <CardTitle className="flex items-center gap-2">
                        Claim ID: {claim.claim_id}
                        {overrideStatus[claim.claim_id] === 'approved' && (
                          <Badge variant="success">Approved</Badge>
                        )}
                        {overrideStatus[claim.claim_id] === 'rejected' && (
                          <Badge variant="destructive">Rejected</Badge>
                        )}
                      </CardTitle>
                      <CardDescription>
                        Assigned to: {claim.assigned_team}
                      </CardDescription>
                    </div>
                    <div className="flex gap-2">
                      <Badge variant={
                        claim.urgency === 'High' ? 'destructive' : 
                        claim.urgency === 'Medium' ? 'warning' : 'success'
                      }>
                        {claim.urgency}
                      </Badge>
                      <Badge variant={
                        claim.customer_value === 'VIP' ? 'default' : 
                        claim.customer_value === 'Premium' ? 'secondary' : 'outline'
                      }>
                        {claim.customer_value}
                      </Badge>
                    </div>
                  </div>
                </CardHeader>
                
                <CardContent>
                  <div className="grid grid-cols-2 gap-4 mb-2">
                    <div>
                      <p className="text-sm font-medium text-gray-500">Risk Score</p>
                      <div className="flex items-center mt-1">
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div 
                            className={`h-2 rounded-full ${
                              claim.risk_score > 0.7 ? 'bg-red-500' : 
                              claim.risk_score > 0.4 ? 'bg-yellow-500' : 'bg-green-500'
                            }`} 
                            style={{ width: `${claim.risk_score * 100}%` }}
                          ></div>
                        </div>
                        <span className="ml-2 text-sm font-medium">{Math.round(claim.risk_score * 100)}%</span>
                      </div>
                    </div>
                    
                    <div>
                      <p className="text-sm font-medium text-gray-500">Claim Amount</p>
                      <p className="font-medium">
                        {claim.claim_data.claim_amount_paid 
                          ? `€${claim.claim_data.claim_amount_paid.toLocaleString()}`
                          : 'N/A'}
                      </p>
                    </div>
                  </div>
                  
                  {expandedClaim === claim.claim_id && (
                    <div className="mt-4 space-y-4">
                      <div>
                        <h4 className="font-medium mb-1">Routing Reasons</h4>
                        <ul className="list-disc pl-5 space-y-1">
                          {claim.reasoning.map((reason, index) => (
                            <li key={index} className="text-sm text-gray-700">{reason}</li>
                          ))}
                        </ul>
                      </div>
                      
                      <div>
                        <h4 className="font-medium mb-1">Claim Details</h4>
                        <div className="grid grid-cols-2 gap-x-4 gap-y-2 text-sm">
                          <div>
                            <span className="text-gray-500">Policyholder Age:</span>{' '}
                            {claim.claim_data.policyholder_age || 'N/A'}
                          </div>
                          <div>
                            <span className="text-gray-500">Warranty:</span>{' '}
                            {claim.claim_data.warranty || 'N/A'}
                          </div>
                          <div>
                            <span className="text-gray-500">Region:</span>{' '}
                            {claim.claim_data.claim_region || 'N/A'}
                          </div>
                          <div>
                            <span className="text-gray-500">Vehicle Brand:</span>{' '}
                            {claim.claim_data.vehicle_brand || 'N/A'}
                          </div>
                          <div>
                            <span className="text-gray-500">Premium Paid:</span>{' '}
                            {claim.claim_data.premium_amount_paid 
                              ? `€${claim.claim_data.premium_amount_paid.toLocaleString()}`
                              : 'N/A'}
                          </div>
                          <div>
                            <span className="text-gray-500">Claim Date:</span>{' '}
                            {claim.claim_data.claim_date || 'N/A'}
                          </div>
                        </div>
                      </div>
                      
                      {claim.claim_data.raw_text && (
                        <div>
                          <h4 className="font-medium mb-1">Original Claim Text</h4>
                          <p className="text-sm text-gray-700 bg-gray-50 p-3 rounded border">
                            {claim.claim_data.raw_text}
                          </p>
                        </div>
                      )}
                      
                      <div className="pt-2">
                        <h4 className="font-medium mb-2">Adjuster Actions</h4>
                        <div className="flex gap-2">
                          <Button 
                            variant="outline" 
                            size="sm"
                            className="flex items-center gap-1"
                            onClick={() => handleOverride(claim.claim_id, 'approved')}
                            disabled={overrideStatus[claim.claim_id] === 'approved'}
                          >
                            <CheckCircle size={16} />
                            Approve Routing
                          </Button>
                          <Button 
                            variant="outline" 
                            size="sm"
                            className="flex items-center gap-1 text-red-600 border-red-200 hover:bg-red-50"
                            onClick={() => handleOverride(claim.claim_id, 'rejected')}
                            disabled={overrideStatus[claim.claim_id] === 'rejected'}
                          >
                            <XCircle size={16} />
                            Reject Routing
                          </Button>
                        </div>
                      </div>
                    </div>
                  )}
                </CardContent>
                
                <CardFooter>
                  <Button 
                    variant="ghost" 
                    size="sm" 
                    onClick={() => toggleClaimExpand(claim.claim_id)}
                  >
                    {expandedClaim === claim.claim_id ? 'Show Less' : 'Show Details'}
                  </Button>
                </CardFooter>
              </Card>
            ))}
            
            {claims.length === 0 && (
              <Card className="py-12">
                <CardContent className="text-center">
                  <p className="text-gray-500">No claims found. Submit a claim to see it here.</p>
                </CardContent>
              </Card>
            )}
          </div>
        </>
      )}
    </div>
  );
};

export default AdjusterDashboardPage;
