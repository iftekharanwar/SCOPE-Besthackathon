from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import claims

app = FastAPI(
    title="Smart Insurance Claim Routing Assistant",
    description="API for routing insurance claims to appropriate teams",
    version="0.1.0"
)

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(claims.router, tags=["claims"])

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.get("/")
async def root():
    return {
        "message": "Welcome to the Smart Insurance Claim Routing Assistant API",
        "endpoints": {
            "submit_claim": "/submit-claim",
            "adjuster_dashboard": "/adjuster-dashboard",
            "get_claim": "/claim/{claim_id}"
        }
    }
