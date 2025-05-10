from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

from app.models.claim import ClaimInput, RoutingDecision
from app.modules.claim_extractor import ClaimExtractor
from app.modules.routing_engine import RoutingEngine
from app.modules.database import ClaimDatabase

router = APIRouter()


@router.post("/submit-claim", response_model=RoutingDecision)
async def submit_claim(claim_input: ClaimInput) -> RoutingDecision:
    """
    Submit a new insurance claim for processing and routing
    
    - Accepts either text or structured JSON data
    - Extracts relevant claim details
    - Analyzes the claim for urgency, risk, and customer value
    - Routes the claim to the appropriate team
    - Returns the routing decision with explanation
    """
    try:
        claim_data = ClaimExtractor.extract(claim_input.dict())
        
        routing_decision = RoutingEngine.route_claim(claim_data)
        
        ClaimDatabase.add_claim(routing_decision)
        
        return routing_decision
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@router.get("/adjuster-dashboard", response_model=List[RoutingDecision])
async def adjuster_dashboard(team: str = None) -> List[RoutingDecision]:
    """
    Get all claims for the adjuster dashboard
    
    - Returns all claims if no team is specified
    - Returns claims for a specific team if team parameter is provided
    """
    if team:
        claims = ClaimDatabase.get_claims_by_team(team)
    else:
        claims = ClaimDatabase.get_all_claims()
    
    return claims


@router.get("/claim/{claim_id}", response_model=RoutingDecision)
async def get_claim(claim_id: str) -> RoutingDecision:
    """
    Get a specific claim by ID
    """
    claim = ClaimDatabase.get_claim_by_id(claim_id)
    if not claim:
        raise HTTPException(status_code=404, detail=f"Claim with ID {claim_id} not found")
    
    return claim
