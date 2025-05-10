import uuid
from app.models.claim import ClaimData, RoutingDecision
from app.modules.scoring_engine import ScoringEngine


class RoutingEngine:
    """Route claims to appropriate teams based on claim data and scores"""

    @staticmethod
    def route_claim(claim_data: ClaimData) -> RoutingDecision:
        """
        Determine the appropriate team for a claim based on its characteristics
        Returns a RoutingDecision with team assignment and reasoning
        """
        urgency_score, urgency_level, urgency_reasons = ScoringEngine.calculate_urgency(claim_data)
        risk_score, risk_reasons = ScoringEngine.calculate_risk(claim_data)
        customer_value, value_reasons = ScoringEngine.calculate_customer_value(claim_data)
        
        all_reasons = urgency_reasons + risk_reasons + value_reasons
        
        assigned_team = RoutingEngine._assign_team(claim_data, urgency_level, risk_score, customer_value)
        
        claim_id = claim_data.claim_id or f"CLAIM-{uuid.uuid4().hex[:8].upper()}"
        
        decision = RoutingDecision(
            assigned_team=assigned_team,
            urgency=urgency_level,
            risk_score=risk_score,
            customer_value=customer_value,
            reasoning=all_reasons,
            claim_data=claim_data,
            claim_id=claim_id
        )
        
        return decision
    
    @staticmethod
    def _assign_team(claim_data: ClaimData, urgency: str, risk_score: float, customer_value: str) -> str:
        """Assign claim to appropriate team based on business rules"""
        
        if claim_data.claim_amount_paid and claim_data.claim_amount_paid > 15000:
            region = claim_data.claim_region or "Central"
            return f"High Value Claims - {region}"
        
        if claim_data.warranty and "third-party" in claim_data.warranty.lower():
            return "Legal Claims Department"
        
        if claim_data.policyholder_age and claim_data.policyholder_age > 60 and claim_data.claim_amount_paid and claim_data.claim_amount_paid > 10000:
            return "Senior High-Risk Claims"
        
        if customer_value == "VIP":
            return "VIP Customer Service"
        
        if claim_data.claim_region in ["Napoli", "Naples", "Caserta"]:
            return "Regional Team - South"
        
        if urgency == "High" and risk_score > 0.7:
            return "Urgent High-Risk Claims"
        elif urgency == "High":
            return "Urgent Claims Processing"
        elif risk_score > 0.7:
            return "High-Risk Claims Processing"
        else:
            return "Standard Claims Processing"
