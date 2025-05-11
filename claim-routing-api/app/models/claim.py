from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class ClaimInput(BaseModel):
    """Model for incoming claim data (either structured or text)"""
    text: Optional[str] = None
    structured_data: Optional[dict] = None


class FraudIndicator(BaseModel):
    """Model for fraud indicators"""
    is_potential_fraud: bool = False
    fraud_score: float = 0.0
    fraud_indicators: List[str] = []


class ClaimData(BaseModel):
    """Model for extracted claim data"""
    policyholder_age: Optional[int] = None
    warranty: Optional[str] = None
    claim_amount_paid: Optional[float] = None
    premium_amount_paid: Optional[float] = None
    claim_region: Optional[str] = None
    claim_province: Optional[str] = None
    vehicle_brand: Optional[str] = None
    vehicle_model: Optional[str] = None
    policyholder_gender: Optional[str] = None
    claim_id: Optional[str] = None
    claim_date: Optional[str] = None
    raw_text: Optional[str] = None
    fraud_indicator: Optional[FraudIndicator] = None


class RoutingDecision(BaseModel):
    """Model for claim routing decision"""
    assigned_team: str
    urgency: str = Field(..., description="Low, Medium, High")
    risk_score: float = Field(..., ge=0, le=1)
    customer_value: str = Field(..., description="Standard, Premium, VIP")
    reasoning: List[str]
    claim_data: ClaimData
    claim_id: str
    is_potential_fraud: bool = False
    fraud_indicators: List[str] = []


class ClaimStore(BaseModel):
    """Model for storing claims in memory"""
    claims: List[RoutingDecision] = []
