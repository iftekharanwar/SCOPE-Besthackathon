# SCOPE Assistant

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

- **Python 3.12+** (specifically tested with Python 3.12.5)
  * Check your version with `python --version`
  * If you have multiple Python versions, ensure you're using 3.12+
  * We recommend using pyenv for Python version management
- **Node.js 16+** with npm/pnpm/yarn
  * Check your version with `node --version`
  * We recommend using nvm for Node.js version management
- **Git**

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/iftekharanwar/smart-insurance-claim-routing.git
   cd smart-insurance-claim-routing
   ```

2. Navigate to the backend directory:
   ```bash
   cd claim-routing-api
   ```

3. Create a Python virtual environment (if not using Poetry):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install dependencies with Poetry:
   ```bash
   # Install Poetry if you don't have it
   # curl -sSL https://install.python-poetry.org | python3 -
   
   # Install dependencies
   poetry install
   
   # If you encounter any issues, try:
   poetry update
   ```

   Or with pip (if not using Poetry):
   ```bash
   pip install fastapi uvicorn pandas numpy scikit-learn python-dotenv spacy
   ```

5. Install spaCy and download the English language model (required for NLP features):
   ```bash
   # With Poetry
   poetry add spacy
   poetry run python -m spacy download en_core_web_sm
   
   # Or with pip
   pip install spacy
   python -m spacy download en_core_web_sm
   ```
   
   **Important Notes about spaCy:**
   - The spaCy installation is **critical** for the NLP text extraction features
   - If you get "No module named 'spacy'" error after installation:
     * Make sure you're in the correct virtual environment
     * Try reinstalling with `pip install --force-reinstall spacy`
   - If you get "No such model: en_core_web_sm" error:
     * The language model download might have failed
     * Try downloading again with `python -m spacy download en_core_web_sm`
     * If that fails, download manually from [spaCy models](https://github.com/explosion/spacy-models/releases/tag/en_core_web_sm-3.8.0)
   - Python version compatibility:
     * spaCy 3.7+ requires Python 3.8+
     * This project uses spaCy 3.7.2 which is compatible with Python 3.12

6. Create a `.env` file in the `claim-routing-api` directory (optional):
   ```
   DEBUG=True
   ```

7. Start the backend server:
   ```bash
   # With Poetry
   poetry run uvicorn app.main:app --reload
   
   # Or with FastAPI CLI (if installed)
   poetry run fastapi dev app/main.py
   
   # Or with plain Python
   python -m uvicorn app.main:app --reload
   ```

8. Troubleshooting common issues:
   - If you get "No module named 'spacy'": Make sure you've installed spaCy and are using the correct virtual environment
   - If you get "No such model: en_core_web_sm": Run the spaCy download command again
   - If you get port conflicts: Change the port with `--port 8001` or another available port

5. The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```

2. Install frontend dependencies:
   ```bash
   # Using npm
   npm install
   
   # Or using pnpm
   pnpm install
   
   # Or using yarn
   yarn install
   ```

3. Create a `.env` file in the frontend directory:
   ```
   # For local development
   VITE_API_URL=http://localhost:8000
   
   # For production (when backend is deployed)
   # VITE_API_URL=https://app-nnlwofep.fly.dev
   ```

4. Start the development server:
   ```bash
   # Using npm
   npm run dev
   
   # Or using pnpm
   pnpm run dev
   
   # Or using yarn
   yarn dev
   ```

5. The frontend will be available at `http://localhost:5173`

6. Troubleshooting frontend issues:
   - If you get dependency errors: Try deleting `node_modules` folder and `package-lock.json` (or `pnpm-lock.yaml`/`yarn.lock`), then reinstall
   - If you get TypeScript errors: Make sure you're using a compatible Node.js version (16+)
   - If the API connection fails: Check that your backend is running and the VITE_API_URL is correct
   - If you see "Module not found" errors: Check that all dependencies are properly installed

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
