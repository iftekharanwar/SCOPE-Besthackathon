# SCOPE-Besthackathon

A prototype AI assistant for the BEST Hackathon that automatically processes insurance claims, extracts relevant details, analyzes risk factors, and routes claims to appropriate departments.

## 🚀 Live Demo

- Backend API: *Coming soon*
- Frontend: *Coming soon*

## 📋 Project Overview

This prototype system:

1. Takes incoming insurance claims (from text or structured data)
2. Automatically extracts relevant claim details (age, warranty type, claim amount, etc.)
3. Analyzes the claim to assess:
   - Urgency level
   - Risk level (fraud potential, complexity)
   - Customer value (based on premium paid)
4. Automatically routes the claim to the right department/team
5. Shows the adjuster team a real-time dashboard with all relevant data and reasoning

## 🏗️ System Architecture

### Backend (Python/FastAPI)

- Claim extraction module for parsing text/JSON inputs
- Scoring engine for calculating urgency, risk, and customer value
- Routing engine for assigning claims to appropriate teams
- In-memory database for storing and retrieving claims

### Frontend (React/TypeScript)

- Claim submission page with text and JSON input options
- Adjuster dashboard with claim listings and filtering
- Visualizations for claim distribution and metrics

## 🛠️ Installation

### Prerequisites

- Python 3.8+ with Poetry
- Node.js 16+ with npm
- Git

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/iftekharanwar/SCOPE-Besthackathon.git
   cd SCOPE-Besthackathon
   ```

2. Install backend dependencies:
   ```bash
   cd claim-routing-api
   poetry install
   ```

3. Create a `.env` file in the `claim-routing-api` directory (optional):
   ```
   DEBUG=True
   ```

4. Start the backend server:
   ```bash
   poetry run fastapi dev app/main.py
   ```

5. The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```

2. Install frontend dependencies:
   ```bash
   npm install
   ```

3. Create a `.env` file in the frontend directory:
   ```
   VITE_API_URL=http://localhost:8000
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

5. The frontend will be available at `http://localhost:5173`

## 🧪 Verification Steps

### Backend Verification

1. Check if the API is running:
   ```bash
   curl http://localhost:8000/
   ```
   You should see a welcome message.

2. Test the claim submission endpoint:
   ```bash
   curl -X POST http://localhost:8000/submit-claim \
     -H "Content-Type: application/json" \
     -d '{"text": "I am a 65-year-old policyholder. I live in Milan. My BMW 5 Series was hit by another vehicle. Claim type: third-party liability. Rear bumper damaged badly. Claim is around €18,000."}'
   ```
   You should receive a JSON response with routing details.

3. Test the dashboard endpoint:
   ```bash
   curl http://localhost:8000/adjuster-dashboard
   ```
   You should receive a list of claims.

### Frontend Verification

1. Open `http://localhost:5173` in your browser
2. Navigate to the "Submit Claim" page
3. Enter a sample claim text or JSON data
4. Submit the claim and verify that the routing result is displayed
5. Navigate to the "Adjuster Dashboard" page
6. Verify that the submitted claim appears in the dashboard

## 📊 Dataset

The system uses the `2025 - BEST Hackathon - dataset.xlsx` file for:
- Deriving business rules for claim routing
- Setting thresholds for urgency, risk, and customer value
- Simulating real-world claim scenarios

## 🔍 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/submit-claim` | POST | Accepts text/JSON claim, returns routed JSON |
| `/adjuster-dashboard` | GET | Returns current assigned claims with analysis |
| `/claim/{claim_id}` | GET | Returns details for a specific claim |

## 📝 Notes

- This is a prototype system using an in-memory database
- Data will be reset when the server restarts
- For production use, a persistent database would be required

## 👥 Contributors

- @iftekharanwar
- @Meirohich
- @KICOEV115
- Created for the 2025 BEST Hackathon

## 📄 License

This project is private and not licensed for public use.


I'll share the deployment steps for both backend and frontend:

### Backend Deployment Steps:
1. Navigate to the backend directory: `cd insurance-claim-assistant/claim-routing-api`
2. Install Fly.io CLI: `curl -L https://fly.io/install.sh | sh`
3. Login to Fly.io: `fly auth login`
4. Initialize deployment: `fly launch --name your-app-name`
5. Deploy: `fly deploy`

### Frontend Deployment Steps:
1. Navigate to frontend directory: `cd insurance-claim-assistant/frontend`
2. Build the app: `npm run build`
3. Deploy to Netlify/Vercel:
   - Install Netlify CLI: `npm install -g netlify-cli`
   - Deploy: `netlify deploy --prod --dir=dist`

NOTE: Regarding customer value calculation: It's determined in `scoring_engine.py` based on premium-to-claim ratio thresholds. Currently, most claims fall into "Standard" because the thresholds are set high (>0.5 for Premium, >1.0 for VIP). You can adjust these thresholds in the `calculate_customer_value` function to get more varied results.
