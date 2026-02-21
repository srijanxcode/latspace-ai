# 🚀 LatSpace AI

> AI-powered Excel Parsing + Parameter Onboarding Platform  
> Built with FastAPI, Streamlit, Gemini 1.5 Flash  
> Fully containerized & deployed on Railway

---

## 🌐 Live Deployment

| Service | Link |
|----------|------|
| 📘 Backend API Docs | https://latspace-ai-production.up.railway.app/docs |
| 📊 Track A — Excel Parser | https://your-track-a-domain.up.railway.app |
| 🧭 Track B — Onboarding Wizard | https://your-track-b-domain.up.railway.app |

> Replace frontend links above with your actual Railway frontend domains.

---

# 🧠 Project Overview

LatSpace AI is a hybrid AI + deterministic system designed to:

- Parse messy Excel datasets intelligently
- Map fuzzy headers to canonical parameters
- Validate formulas and structured onboarding inputs
- Provide context-aware AI suggestions
- Ensure strict schema validation via Pydantic

This project demonstrates **LLM integration done responsibly** — using AI only where semantic reasoning is required.

---

# 🎯 Track A — Excel Parser

### 🔍 What It Does
- Upload messy multi-sheet Excel files
- Uses Gemini to map headers → canonical parameters
- Deterministic Python parsing for values
- Schema validation via Pydantic
- Duplicate detection across sheets
- Structured JSON output

### 🏗 Design Principles
- ✅ One LLM call per sheet (NOT per column or cell)
- ✅ LLM only for semantic header mapping
- ✅ Deterministic value parsing (cost-efficient)
- ✅ Strict schema validation
- ✅ Multi-sheet support

---

# 🧭 Track B — Onboarding Wizard

### 🔍 What It Does
- Guided multi-step onboarding flow
- Parameter registry selection
- Formula validation
- Context-aware Gemini suggestions
- Structured submission payload

### ⚙️ Technical Highlights
- FastAPI validation layer
- Typed Pydantic request/response models
- Controlled temperature strategy
- Deterministic + creative hybrid architecture

---

# 🤖 LLM Configuration

**Model:** Google Gemini 1.5 Flash  

Why this model?
- Fast
- Free-tier friendly
- Strong JSON instruction following
- Cost efficient

### 🎛 Temperature Strategy
- `0.1` → Deterministic mapping (Track A)
- `0.3` → Creative suggestions (Track B)

---

# 🏗 System Architecture

```
latspace-ai/
├── backend/
│   ├── app/
│   │   ├── agents/         # Gemini LLM agents
│   │   ├── models/         # Pydantic schemas
│   │   ├── routers/        # FastAPI endpoints
│   │   └── utils/          # Registry loader, value parser
│   ├── registry/           # parameters.json, assets.json
│   └── test_data/          # Sample .xlsx files
├── frontend/
│   ├── track_a/            # Excel Parser UI (Streamlit)
│   └── track_b/            # Onboarding Wizard UI (Streamlit)
└── docker-compose.yml
```

---

# 🔐 Environment Configuration

Environment variables (Railway or local):

```
GEMINI_API_KEY=your_api_key
GEMINI_MODEL=gemini-1.5-flash
```

Backend listens on dynamic `$PORT` for Railway compatibility.

---

# 🧪 Local Development (Docker)

```bash
# Clone repo
git clone https://github.com/srijanxcode/latspace-ai.git
cd latspace-ai

# Create environment file
cp .env.example .env
# Add your GEMINI_API_KEY inside .env

# Build containers
make build

# Start services
make up

# Generate sample Excel files
make create-test-data
```

### Local URLs

| Service | URL |
|----------|------|
| Backend Docs | http://localhost:8000/docs |
| Track A UI | http://localhost:8501 |
| Track B UI | http://localhost:8502 |

---

# 💡 Key Engineering Decisions

- Hybrid AI + deterministic design
- No LLM per-cell calls (cost control)
- Pydantic everywhere for strict validation
- Clean separation of concerns
- Containerized for portability
- Railway-ready deployment configuration

---

# 🚀 Production Deployment

- Backend deployed on Railway
- Frontends deployed as separate Railway services
- Uses dynamic PORT binding
- Environment variables managed securely

---

# 🔮 Future Improvements

- Chunked streaming for very large files (>1000 rows)
- Persistent wizard sessions (SQLite / Redis)
- Unit tests for parser & validator
- Caching header mappings
- CI/CD integration
- Usage analytics

---

# 📌 Summary

LatSpace AI demonstrates:

- Thoughtful LLM usage
- Strong backend architecture
- Full-stack integration
- Cost-efficient AI design
- Production-ready deployment

This is not just an LLM demo — it’s a system-level engineering solution.