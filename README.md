# 🚀 LatSpace AI

> AI-Powered Excel Parsing + Parameter Onboarding Platform  
> Built with FastAPI • Streamlit • Gemini 1.5 Flash  
> Fully containerized & deployed on Railway

---

## 🌐 Live Deployment

| Service | Link |
|----------|------|
| 📘 Backend API Docs | https://latspace-ai-production.up.railway.app/docs |
| 📊 Track A — Excel Parser | https://amused-happiness-production.up.railway.app |
| 🧭 Track B — Onboarding Wizard | https://diligent-luck-production.up.railway.app |

---

# 🧠 Project Overview

LatSpace AI is a hybrid AI + deterministic system designed to intelligently onboard structured data from messy sources.

It demonstrates how to use LLMs responsibly in production systems by:

- Using AI only where semantic reasoning is required
- Keeping value parsing deterministic
- Strictly validating all outputs
- Minimizing LLM cost with optimized call design

This is not just an LLM demo — it’s a system-level engineering solution.

---

# 🎯 Track A — Excel Parser

### 🔍 What It Does

- Upload messy multi-sheet Excel files
- Uses Gemini to map fuzzy headers → canonical parameter names
- Parses values deterministically in Python
- Validates structure using Pydantic
- Detects duplicates across sheets
- Returns structured JSON output

### 🏗 Design Principles

- ✅ **One LLM call per sheet** (NOT per column or per cell)
- ✅ LLM only for semantic header mapping
- ✅ Deterministic parsing for all values
- ✅ Strict schema validation
- ✅ Multi-sheet support

This keeps cost low while maintaining intelligent mapping capability.

---

# 🧭 Track B — Onboarding Wizard

### 🔍 What It Does

- Guided multi-step onboarding flow
- Parameter registry selection
- Formula validation
- Context-aware AI suggestions via Gemini
- Structured submission payload

### ⚙️ Technical Highlights

- FastAPI validation layer
- Strongly typed Pydantic request/response models
- Controlled temperature strategy
- Hybrid deterministic + AI-driven logic

---

# 🤖 LLM Configuration

**Model:** Google Gemini 1.5 Flash  

Why this model?

- Fast
- Free-tier friendly
- Strong JSON instruction following
- Reliable structured outputs

### 🎛 Temperature Strategy

- `0.1` → Deterministic header mapping (Track A)
- `0.3` → Suggestion generation (Track B)

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
# Clone repository
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
- No per-cell LLM calls (cost control)
- Pydantic validation everywhere
- Clean separation of concerns
- Containerized architecture
- Railway-ready deployment configuration

---

# 🚀 Production Deployment

- Backend deployed as Railway service
- Track A and Track B deployed as separate Railway services
- Dynamic port binding
- Secure environment variable handling
- Independent scaling per service

---

# 🔮 Future Improvements

- Chunked streaming for very large files (>1000 rows)
- Persistent wizard sessions (SQLite / Redis)
- Unit tests for parser & validator
- Caching header mappings
- CI/CD integration
- Usage analytics & monitoring

---

# 📌 Summary

LatSpace AI demonstrates:

- Practical LLM integration
- Clean backend architecture
- Full-stack system design
- Cost-efficient AI usage
- Production-ready deployment

This project showcases thoughtful engineering — not just API calls.