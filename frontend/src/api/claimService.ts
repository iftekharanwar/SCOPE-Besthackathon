import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface ClaimInput {
  text?: string;
  structured_data?: Record<string, any>;
}

export interface ClaimData {
  policyholder_age?: number;
  warranty?: string;
  claim_amount_paid?: number;
  premium_amount_paid?: number;
  claim_region?: string;
  claim_province?: string;
  vehicle_brand?: string;
  vehicle_model?: string;
  policyholder_gender?: string;
  claim_id?: string;
  claim_date?: string;
  raw_text?: string;
}

export interface RoutingDecision {
  assigned_team: string;
  urgency: string;
  risk_score: number;
  customer_value: string;
  reasoning: string[];
  claim_data: ClaimData;
  claim_id: string;
}

export const submitClaim = async (claimInput: ClaimInput): Promise<RoutingDecision> => {
  try {
    const response = await axios.post(`${API_URL}/submit-claim`, claimInput);
    return response.data;
  } catch (error) {
    console.error('Error submitting claim:', error);
    throw error;
  }
};

export const getAdjusterDashboard = async (team?: string): Promise<RoutingDecision[]> => {
  try {
    const url = team 
      ? `${API_URL}/adjuster-dashboard?team=${encodeURIComponent(team)}` 
      : `${API_URL}/adjuster-dashboard`;
    
    const response = await axios.get(url);
    return response.data;
  } catch (error) {
    console.error('Error fetching adjuster dashboard:', error);
    throw error;
  }
};

export const getClaimById = async (claimId: string): Promise<RoutingDecision> => {
  try {
    const response = await axios.get(`${API_URL}/claim/${claimId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching claim ${claimId}:`, error);
    throw error;
  }
};
