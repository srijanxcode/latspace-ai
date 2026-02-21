---

## 🎯 Track A — Excel Parser

### What It Does
- Upload messy multi-sheet Excel files
- Uses Gemini to map headers → canonical parameters
- Parses values deterministically
- Validates structure using Pydantic
- Detects duplicates across sheets

### Design Principles
- ✅ One LLM call per sheet (not per column)
- ✅ LLM only for semantic mapping
- ✅ Deterministic Python parsing for values
- ✅ Strict schema validation

---

## 🧭 Track B — Onboarding Wizard

### What It Does
- Guided multi-step wizard
- Parameter selection
- Formula validation
- Context-aware suggestions via Gemini
- Final structured submission

### Technical Highlights
- FastAPI validation layer
- Pydantic request/response models
- Controlled temperature (0.1 mapping, 0.3 suggestions)

---

## 🤖 LLM Configuration

**Model:** Google Gemini 1.5 Flash  
- Fast  
- Free tier friendly  
- Strong JSON instruction following  

Temperature Strategy:
- 0.1 → Deterministic mapping
- 0.3 → Suggestion generation

---

## 🔐 Security & Environment

Environment Variables (Railway):latspace-ai/
├── backend/
│   ├── app/
│   │   ├── agents/         # Gemini LLM agents
│   │   ├── models/         # Pydantic schemas
│   │   ├── routers/        # FastAPI endpoints
│   │   └── utils/          # Registry loader, value parser
│   ├── registry/           # parameters.json, assets.json
│   └── test_data/          # Generated .xlsx test files
├── frontend/
│   ├── track_a/            # Excel Parser (Streamlit UI)
│   └── track_b/            # Onboarding Wizard (Streamlit UI)
└── docker-compose.yml---

## 🎯 Track A — Excel Parser

### What It Does
- Upload messy multi-sheet Excel files
- Uses Gemini to map headers → canonical parameters
- Parses values deterministically
- Validates structure using Pydantic
- Detects duplicates across sheets

### Design Principles
- ✅ One LLM call per sheet (not per column)
- ✅ LLM only for semantic mapping
- ✅ Deterministic Python parsing for values
- ✅ Strict schema validation

---

## 🧭 Track B — Onboarding Wizard

### What It Does
- Guided multi-step wizard
- Parameter selection
- Formula validation
- Context-aware suggestions via Gemini
- Final structured submission

### Technical Highlights
- FastAPI validation layer
- Pydantic request/response models
- Controlled temperature (0.1 mapping, 0.3 suggestions)

---

## 🤖 LLM Configuration

**Model:** Google Gemini 1.5 Flash  
- Fast  
- Free tier friendly  
- Strong JSON instruction following  

Temperature Strategy:
- 0.1 → Deterministic mapping
- 0.3 → Suggestion generation

---

## 🔐 Security & Environment

Environment Variables (Railway):Backend listens on dynamic `$PORT` for Railway compatibility.

---

## 🧪 Local Development (Docker)

```bash
# Clone repo
git clone <your-repo-url>
cd latspace-ai

# Create environment file
cp .env.example .env
# Add your GEMINI_API_KEY

# Build and run
make build
make up

# Generate sample Excel files
make create-test-data