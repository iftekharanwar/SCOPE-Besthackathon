from typing import List, Optional
import uuid
from app.models.claim import RoutingDecision, ClaimStore

claim_store = ClaimStore(claims=[])


class ClaimDatabase:
    """In-memory database for storing and retrieving claims"""
    
    @staticmethod
    def add_claim(claim: RoutingDecision) -> RoutingDecision:
        """Add a claim to the database"""
        if not claim.claim_id:
            claim.claim_id = f"CLAIM-{uuid.uuid4().hex[:8].upper()}"
            
        claim_store.claims.append(claim)
        return claim
    
    @staticmethod
    def get_all_claims() -> List[RoutingDecision]:
        """Get all claims from the database"""
        return claim_store.claims
    
    @staticmethod
    def get_claim_by_id(claim_id: str) -> Optional[RoutingDecision]:
        """Get a claim by its ID"""
        for claim in claim_store.claims:
            if claim.claim_id == claim_id:
                return claim
        return None
    
    @staticmethod
    def get_claims_by_team(team: str) -> List[RoutingDecision]:
        """Get all claims assigned to a specific team"""
        return [claim for claim in claim_store.claims if claim.assigned_team == team]
