# Smart Insurance Claim Routing Assistant - Technical Documentation

## 1. System Overview

The Smart Insurance Claim Routing Assistant is a **prototype** system designed to automate the processing and routing of insurance claims. It demonstrates how AI and rule-based systems can be used to extract information from claim submissions, analyze risk factors, and route claims to appropriate departments.

**Important Note**: This is a prototype implementation with an in-memory database. In a production environment, this would be replaced with a persistent database system and additional security measures.

## 2. System Architecture

The system follows a modern microservices architecture with a clear separation between frontend and backend components:

```
┌─────────────────┐      ┌──────────────────────────────────────┐
│                 │      │                                      │
│    Frontend     │◄────►│               Backend                │
│  (React/TypeScript) │      │             (FastAPI/Python)           │
│                 │      │                                      │
└─────────────────┘      └──────────────────────────────────────┘
        │                                   │
        │                                   │
        ▼                                   ▼
┌─────────────────┐      ┌──────────────────────────────────────┐
│  User Interface │      │           Business Logic             │
│  - Claim Form   │      │  - Claim Extraction                  │
│  - Dashboard    │      │  - Scoring Engine                    │
│                 │      │  - Routing Engine                    │
└─────────────────┘      └──────────────────────────────────────┘
                                           │
                                           │
                                           ▼
                         ┌──────────────────────────────────────┐
                         │            Data Storage              │
                         │  - In-memory Database (Prototype)    │
                         │  (Would be replaced with persistent  │
                         │   storage in production)             │
                         └──────────────────────────────────────┘
```

### 2.1 Backend Architecture

The backend is built with FastAPI, a modern, high-performance web framework for building APIs with Python. It follows a modular architecture:

```
claim-routing-api/
├── app/
│   ├── main.py                # Application entry point
│   ├── models/                # Data models
│   │   └── claim.py           # Claim data model
│   ├── modules/               # Business logic modules
│   │   ├── claim_extractor.py # Extracts claim data from text/JSON
│   │   ├── database.py        # In-memory database implementation
│   │   ├── routing_engine.py  # Routes claims to departments
│   │   └── scoring_engine.py  # Calculates risk, urgency, value scores
│   └── routers/               # API route definitions
│       └── claims.py          # Claim-related endpoints
├── pyproject.toml             # Project dependencies
└── tests/                     # Unit tests
```

### 2.2 Frontend Architecture

The frontend is built with React and TypeScript, using a component-based architecture:

```
frontend/
├── public/                    # Static assets
├── src/
│   ├── api/                   # API service layer
│   │   └── claimService.ts    # API client for backend communication
│   ├── components/            # Reusable UI components
│   │   └── ui/                # Base UI components
│   ├── pages/                 # Page components
│   │   ├── ClaimSubmissionPage.tsx  # Claim submission form
│   │   └── AdjusterDashboardPage.tsx # Adjuster dashboard
│   ├── App.tsx                # Main application component
│   └── main.tsx               # Application entry point
├── package.json               # Project dependencies
└── vite.config.ts             # Build configuration
```

## 3. Data Flow

The system processes data through the following flow:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│             │     │             │     │             │     │             │
│  User Input │────►│ Extraction  │────►│  Analysis   │────►│   Routing   │
│             │     │             │     │             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                          │                   │                   │
                          ▼                   ▼                   ▼
                    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
                    │  Extract    │     │ Calculate   │     │ Determine   │
                    │  relevant   │     │ urgency,    │     │ appropriate │
                    │  claim data │     │ risk, value │     │ department  │
                    └─────────────┘     └─────────────┘     └─────────────┘
                                                                  │
                                                                  │
                                                                  ▼
                                                            ┌─────────────┐
                                                            │ Store and   │
                                                            │ display     │
                                                            │ results     │
                                                            └─────────────┘
```

### 3.1 Detailed Process Flow

1. **Claim Submission**:
   - User submits a claim via text description or structured JSON
   - Frontend sends data to backend API

2. **Claim Extraction**:
   - Backend parses the input (text or JSON)
   - Extracts relevant fields (age, warranty, claim amount, etc.)
   - For text input, uses NLP techniques to identify key information

3. **Claim Analysis**:
   - Calculates urgency score based on:
     - Claim amount
     - Policyholder age
     - Warranty type
   - Calculates risk score based on:
     - Vehicle brand/model
     - Claim region
     - Claim amount
   - Calculates customer value based on:
     - Premium amount paid
     - Policyholder history

4. **Claim Routing**:
   - Applies business rules to determine the appropriate department
   - Generates reasoning for the routing decision
   - Creates a structured routing decision object

5. **Data Storage**:
   - Stores the claim and routing decision in the database
   - For the prototype, this is an in-memory database
   - In production, this would be a persistent database

6. **Result Display**:
   - Returns routing decision to frontend
   - Frontend displays the decision with explanations
   - Claim is added to the adjuster dashboard

## 4. Component Details

### 4.1 Claim Extractor

The claim extractor module is responsible for parsing input data and extracting relevant claim information:

- For text input:
  - Uses pattern matching and NLP techniques to identify key information
  - Extracts policyholder age, warranty type, claim amount, etc.
  - Handles variations in text format and language

- For JSON input:
  - Validates the input structure
  - Maps fields to the internal claim model
  - Handles missing or invalid fields

Key implementation details:
```python
# Simplified example from claim_extractor.py
def extract_from_text(text: str) -> ClaimData:
    # Extract age using regex patterns
    age_match = re.search(r'(\d+)[\s-]*year[\s-]*old', text, re.IGNORECASE)
    age = int(age_match.group(1)) if age_match else None
    
    # Extract warranty type
    warranty_match = re.search(r'warranty:?\s*([^\.,:;]+)', text, re.IGNORECASE)
    warranty = warranty_match.group(1).strip() if warranty_match else None
    
    # Extract claim amount
    amount_match = re.search(r'€?\s*(\d+[,\d]*)', text)
    claim_amount = float(amount_match.group(1).replace(',', '')) if amount_match else None
    
    # Additional extractions...
    
    return ClaimData(
        policyholder_age=age,
        warranty=warranty,
        claim_amount_paid=claim_amount,
        # Other fields...
    )
```

### 4.2 Scoring Engine

The scoring engine calculates three key metrics for each claim:

1. **Urgency Score**:
   - High claim amounts (>€15,000) increase urgency
   - Elderly policyholders (>60 years) increase urgency
   - Third-party liability claims increase urgency

2. **Risk Score**:
   - Luxury vehicle brands increase risk
   - High-risk regions increase risk
   - High claim amounts increase risk
   - Complex warranty types increase risk

3. **Customer Value**:
   - Based primarily on premium amount paid
   - VIP customers (premium >€1,000) receive higher value score
   - Long-term customers receive higher value score

Key implementation details:
```python
# Simplified example from scoring_engine.py
def calculate_urgency(claim_data: ClaimData) -> str:
    score = 0
    
    # High claim amount
    if claim_data.claim_amount_paid and claim_data.claim_amount_paid > 15000:
        score += 3
    elif claim_data.claim_amount_paid and claim_data.claim_amount_paid > 10000:
        score += 2
    
    # Elderly policyholder
    if claim_data.policyholder_age and claim_data.policyholder_age > 60:
        score += 2
    
    # Third-party liability
    if claim_data.warranty and "third-party" in claim_data.warranty.lower():
        score += 2
    
    # Determine urgency level
    if score >= 4:
        return "High"
    elif score >= 2:
        return "Medium"
    else:
        return "Low"
```

### 4.3 Routing Engine

The routing engine applies business rules to determine the appropriate department for each claim:

- **High Value Claims Team**:
  - Claims over €15,000
  - VIP customers with claims over €10,000

- **Legal Claims Department**:
  - Third-party liability claims
  - Claims with potential legal implications

- **Regional Teams**:
  - Claims from specific regions are routed to regional teams
  - Example: Claims from Milan go to "High Value Claims - Milan"

- **Standard Claims Processing**:
  - Default for claims that don't meet specialized criteria

Key implementation details:
```python
# Simplified example from routing_engine.py
def determine_team(claim_data: ClaimData, urgency: str, risk_score: float, customer_value: str) -> str:
    # High value claims
    if claim_data.claim_amount_paid and claim_data.claim_amount_paid > 15000:
        if claim_data.claim_region and "Milan" in claim_data.claim_region:
            return "High Value Claims - Milan"
        return "High Value Claims Team"
    
    # Legal claims
    if claim_data.warranty and "third-party" in claim_data.warranty.lower():
        return "Legal Claims Department"
    
    # Regional routing
    if claim_data.claim_region:
        if "Naples" in claim_data.claim_region or "Napoli" in claim_data.claim_region:
            return "Regional Team - South"
        if "Milan" in claim_data.claim_region or "Milano" in claim_data.claim_region:
            return "Regional Team - North"
    
    # VIP customers
    if customer_value == "VIP":
        return "VIP Customer Service"
    
    # Default routing
    return "Standard Claims Processing"
```

### 4.4 In-Memory Database

The prototype uses an in-memory database to store claims and routing decisions:

- Claims are stored with unique IDs
- Database is reset when the server restarts
- Provides basic query functionality for the adjuster dashboard

Key implementation details:
```python
# Simplified example from database.py
class InMemoryDatabase:
    def __init__(self):
        self.claims = {}
        self.next_id = 1
    
    def add_claim(self, routing_decision: RoutingDecision) -> str:
        claim_id = f"CLM-{self.next_id:06d}"
        self.next_id += 1
        
        routing_decision.claim_id = claim_id
        self.claims[claim_id] = routing_decision
        
        return claim_id
    
    def get_claim(self, claim_id: str) -> Optional[RoutingDecision]:
        return self.claims.get(claim_id)
    
    def get_all_claims(self) -> List[RoutingDecision]:
        return list(self.claims.values())
    
    def get_claims_by_team(self, team: str) -> List[RoutingDecision]:
        return [claim for claim in self.claims.values() if claim.assigned_team == team]
```

## 5. API Endpoints

The backend exposes the following RESTful API endpoints:

### 5.1 Submit Claim

- **Endpoint**: `/submit-claim`
- **Method**: POST
- **Description**: Processes a new claim and returns routing decision
- **Request Body**:
  ```json
  {
    "text": "I'm a 65-year-old policyholder. I live in Milan. My BMW 5 Series was hit by another vehicle. Claim type: third-party liability. Rear bumper damaged badly. Claim is around €18,000."
  }
  ```
  OR
  ```json
  {
    "structured_data": {
      "POLICYHOLDER_AGE": 65,
      "WARRANTY": "third-party liability",
      "CLAIM_AMOUNT_PAID": 18000,
      "PREMIUM_AMOUNT_PAID": 1200,
      "CLAIM_REGION": "Milan",
      "VEHICLE_BRAND": "BMW"
    }
  }
  ```
- **Response**:
  ```json
  {
    "assigned_team": "High Value Claims - Milan",
    "urgency": "High",
    "risk_score": 0.86,
    "customer_value": "VIP",
    "reasoning": [
      "Claim amount > €15,000",
      "Vehicle brand = BMW",
      "Warranty type = Third-party liability",
      "Policyholder age = 65"
    ],
    "claim_data": {
      "policyholder_age": 65,
      "warranty": "third-party liability",
      "claim_amount_paid": 18000,
      "premium_amount_paid": 1200,
      "claim_region": "Milan",
      "vehicle_brand": "BMW"
    },
    "claim_id": "CLM-000001"
  }
  ```

### 5.2 Adjuster Dashboard

- **Endpoint**: `/adjuster-dashboard`
- **Method**: GET
- **Description**: Returns all claims for the adjuster dashboard
- **Query Parameters**:
  - `team` (optional): Filter claims by assigned team
- **Response**:
  ```json
  [
    {
      "assigned_team": "High Value Claims - Milan",
      "urgency": "High",
      "risk_score": 0.86,
      "customer_value": "VIP",
      "reasoning": ["Claim amount > €15,000", "..."],
      "claim_data": { "..." },
      "claim_id": "CLM-000001"
    },
    {
      "assigned_team": "Legal Claims Department",
      "urgency": "Medium",
      "risk_score": 0.65,
      "customer_value": "Standard",
      "reasoning": ["Warranty type = Third-party liability", "..."],
      "claim_data": { "..." },
      "claim_id": "CLM-000002"
    }
  ]
  ```

### 5.3 Get Claim by ID

- **Endpoint**: `/claim/{claim_id}`
- **Method**: GET
- **Description**: Returns details for a specific claim
- **Path Parameters**:
  - `claim_id`: ID of the claim to retrieve
- **Response**: Same as the submit claim response

## 6. Frontend Components

### 6.1 Claim Submission Page

The claim submission page allows users to submit claims in two formats:

1. **Text Input**:
   - Natural language description of the claim
   - Example button to load a sample claim
   - Submit button to process the claim

2. **JSON Input**:
   - Structured JSON data with claim fields
   - Pre-filled with a sample JSON structure
   - Submit button to process the claim

After submission, the page displays the routing decision with:
- Assigned team
- Urgency level (with color coding)
- Risk score (with visual indicator)
- Customer value classification
- Reasoning for the routing decision

### 6.2 Adjuster Dashboard

The adjuster dashboard displays all processed claims with:

- Filterable list of claims by team
- Summary statistics (claims by urgency, team, etc.)
- Detailed view of each claim
- Ability to expand claim details

The dashboard includes visualizations:
- Distribution of claims by urgency
- Distribution of claims by team
- Risk score distribution

## 7. Prototype Limitations

As a prototype, the system has several limitations that would be addressed in a production implementation:

1. **In-Memory Database**:
   - Data is lost when the server restarts
   - No persistence across deployments
   - Limited scalability

2. **Limited NLP Capabilities**:
   - Basic pattern matching for text extraction
   - No advanced NLP models for better understanding
   - Limited language support (primarily English)

3. **Rule-Based Routing**:
   - Fixed business rules rather than ML-based routing
   - Limited ability to adapt to new patterns
   - No feedback loop for improving routing decisions

4. **Security Considerations**:
   - No authentication or authorization
   - No input validation beyond basic parsing
   - No encryption for sensitive data

5. **Performance Limitations**:
   - Not optimized for high throughput
   - No caching mechanisms
   - Limited error handling and recovery

## 8. Production Considerations

For a production implementation, the following enhancements would be recommended:

1. **Persistent Database**:
   - Replace in-memory storage with a proper database (PostgreSQL, MongoDB)
   - Implement data backup and recovery
   - Add database migration capabilities

2. **Advanced NLP**:
   - Integrate with more sophisticated NLP models
   - Support multiple languages
   - Improve extraction accuracy with ML techniques

3. **Machine Learning Routing**:
   - Train ML models on historical data
   - Implement feedback loops to improve routing
   - Add anomaly detection for fraud prevention

4. **Security Enhancements**:
   - Add authentication and authorization
   - Implement input validation and sanitization
   - Add encryption for sensitive data
   - Implement audit logging

5. **Scalability Improvements**:
   - Containerize the application (Docker)
   - Implement horizontal scaling
   - Add load balancing
   - Optimize performance

6. **Monitoring and Logging**:
   - Add comprehensive logging
   - Implement monitoring and alerting
   - Add performance metrics
   - Set up error tracking

## 9. Conclusion

SCOPE - The Smart Insurance Claim Routing Assistant prototype demonstrates the potential for automating insurance claim processing and routing. While it has limitations as a prototype, it provides a solid foundation for developing a production-ready system.

The modular architecture allows for easy extension and enhancement, and the clear separation of concerns makes it straightforward to replace components with more sophisticated implementations as needed.

This prototype serves as a proof of concept for how AI and rule-based systems can be combined to improve efficiency and accuracy in insurance claim processing.
