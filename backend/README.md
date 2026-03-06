# AI Sustainable Commerce API

**Role:** Full Stack / AI Intern | **Focus:** Applied AI for Sustainable Commerce

A production-ready Python/FastAPI application implementing AI-powered modules for sustainable B2B commerce using the **Google Gemini API**.

---

## Modules Implemented

### ✅ Module 1: AI Auto-Category & Tag Generator (Full Implementation)
Automatically categorises products with:
- Primary category (from predefined list of 10)
- Sub-category suggestion
- 5–10 SEO tags
- Applicable sustainability filters (plastic-free, vegan, recycled, etc.)
- Structured JSON output stored in SQLite

### ✅ Module 2: AI B2B Proposal Generator (Full Implementation)
Generates complete sustainable procurement proposals with:
- Recommended sustainable product mix (3–6 items)
- Budget allocation breakdown (within provided limit)
- Estimated cost breakdown (subtotal, packaging, logistics, platform fee)
- Impact positioning summary
- Structured JSON output stored in SQLite

### 📐 Module 3: AI Impact Reporting Generator (Architecture)
See [`architecture.md`](./architecture.md) for full design — DB schema, Gemini prompt strategy, and API endpoints.

### 📐 Module 4: AI WhatsApp Support Bot (Architecture)
See [`architecture.md`](./architecture.md) for full design — intent routing, Twilio/Meta integration, escalation logic, and conversation logging.

---

## Project Structure

```
Dipak_assignment/
├── .env.example            # Environment variable template
├── requirements.txt        # Python dependencies
├── architecture.md         # Module 3 & 4 architecture docs
├── app/
│   ├── main.py             # FastAPI entry point
│   ├── config.py           # Settings + predefined lists
│   ├── database.py         # SQLite init + helpers
│   ├── logger.py           # AI prompt/response logger
│   ├── models/
│   │   ├── product.py      # Module 1 Pydantic models
│   │   └── proposal.py     # Module 2 Pydantic models
│   ├── services/
│   │   ├── gemini.py       # Gemini API client wrapper
│   │   ├── categorizer.py  # Module 1 business logic
│   │   └── proposal_gen.py # Module 2 business logic
│   └── routers/
│       ├── catalog.py      # Module 1 API endpoints
│       └── proposals.py    # Module 2 API endpoints
└── tests/
    ├── test_module1.py
    └── test_module2.py
```

---

## Quick Start

### 1. Clone & enter the project
```bash
git clone <repo-url>
cd Dipak_assignment
```

### 2. Create and activate the virtual environment
```bash
python3 -m venv venv
source venv/bin/activate       # Linux/macOS
# venv\Scripts\activate        # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
```bash
cp .env.example .env
# Edit .env and add your Gemini API key
```

```env
GEMINI_API_KEY=your_gemini_api_key_here
DB_PATH=sustainable_commerce.db
LOG_LEVEL=INFO
```

Get a free Gemini API key at: https://aistudio.google.com/app/apikey

### 5. Run the server
```bash
uvicorn app.main:app --reload
```

The API will be available at: **http://localhost:8000**  
Interactive docs (Swagger UI): **http://localhost:8000/docs**

---

## API Reference

### Health Check
```
GET /health
```

---

### Module 1 — AI Auto-Category & Tag Generator

#### Categorize a product
```
POST /api/v1/catalog/categorize
```
**Request body:**
```json
{
  "name": "Bamboo Toothbrush",
  "description": "Eco-friendly bamboo toothbrush with BPA-free soft bristles. Fully biodegradable."
}
```
**Response:**
```json
{
  "product_id": "a1b2c3...",
  "name": "Bamboo Toothbrush",
  "description": "...",
  "primary_category": "Personal Care",
  "sub_category": "Oral Hygiene",
  "seo_tags": ["bamboo toothbrush", "eco-friendly toothbrush", "biodegradable toothbrush", "..."],
  "sustainability_filters": ["plastic-free", "biodegradable", "vegan"],
  "raw_ai_response": "...",
  "created_at": "2025-04-22T10:00:00Z"
}
```

#### List all categorized products
```
GET /api/v1/catalog/products
```

#### Get a single product
```
GET /api/v1/catalog/products/{product_id}
```

---

### Module 2 — AI B2B Proposal Generator

#### Generate a B2B proposal
```
POST /api/v1/proposals/generate
```
**Request body:**
```json
{
  "company_name": "GreenCorp Solutions",
  "industry": "Corporate Gifting",
  "budget": 50000,
  "preferences": ["plastic-free", "vegan", "recycled"],
  "quantity_needed": 100,
  "use_case": "Employee gifting for Earth Day 2025"
}
```
**Response:**
```json
{
  "proposal_id": "x1y2z3...",
  "company_name": "GreenCorp Solutions",
  "total_budget": 50000,
  "product_mix": [
    {
      "product_name": "Recycled Notebook",
      "category": "Stationery & Office",
      "sustainability_attributes": ["recycled", "plastic-free"],
      "quantity": 50,
      "unit_price": 150.0,
      "total_price": 7500.0,
      "reason": "Perfect for corporate gifting..."
    }
  ],
  "budget_allocation": { "Recycled Notebook": 7500.0 },
  "estimated_cost_breakdown": {
    "subtotal": 11500.0,
    "packaging": 500.0,
    "logistics": 800.0,
    "platform_fee": 200.0,
    "total": 13000.0
  },
  "impact_summary": "This procurement avoids ~2.5 kg of plastic waste...",
  "created_at": "2025-04-22T10:05:00Z"
}
```

#### List all proposals
```
GET /api/v1/proposals/
```

#### Get a single proposal
```
GET /api/v1/proposals/{proposal_id}
```

---

## Running Tests

```bash
# Activate venv first
source venv/bin/activate

python -m pytest tests/ -v
```

Tests use mocked Gemini responses — no real API calls needed.

---

## Technical Design

| Requirement | Implementation |
|---|---|
| Structured JSON outputs | Pydantic models + Gemini JSON-mode prompts |
| Prompt + response logging | `ai_logs` SQLite table via `app/logger.py` |
| Environment-based API key | `.env` loaded via `python-dotenv` in `config.py` |
| Clear separation of AI & business logic | `services/` (AI) ↔ `routers/` (HTTP) ↔ `models/` (schema) |
| Error handling & validation | Pydantic validation + `try/except` → HTTP 500 with detail |

### Predefined Categories (Module 1)
`Food & Beverage` · `Personal Care` · `Home & Living` · `Clothing & Apparel` · `Electronics` · `Stationery & Office` · `Fitness & Wellness` · `Pet Supplies` · `Baby & Kids` · `Outdoor & Garden`

### Sustainability Filters (Module 1)
`plastic-free` · `compostable` · `vegan` · `recycled` · `organic` · `zero-waste` · `fair-trade` · `biodegradable` · `carbon-neutral` · `locally-sourced`

---

## Database Schema

```sql
-- AI call logging (all modules)
CREATE TABLE ai_logs (
    id          TEXT PRIMARY KEY,
    module      TEXT,
    prompt      TEXT,
    response    TEXT,
    latency_ms  INTEGER,
    created_at  TEXT
);

-- Module 1: categorised products
CREATE TABLE products (
    product_id              TEXT PRIMARY KEY,
    name                    TEXT,
    description             TEXT,
    primary_category        TEXT,
    sub_category            TEXT,
    seo_tags                TEXT,  -- JSON array
    sustainability_filters  TEXT,  -- JSON array
    raw_ai_response         TEXT,
    created_at              TEXT
);

-- Module 2: B2B proposals
CREATE TABLE proposals (
    proposal_id      TEXT PRIMARY KEY,
    company_name     TEXT,
    industry         TEXT,
    total_budget     REAL,
    preferences      TEXT,  -- JSON array
    quantity_needed  INTEGER,
    use_case         TEXT,
    product_mix      TEXT,  -- JSON array
    budget_allocation  TEXT,  -- JSON object
    cost_breakdown   TEXT,  -- JSON object
    impact_summary   TEXT,
    raw_ai_response  TEXT,
    created_at       TEXT
);
```

---

## Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `GEMINI_API_KEY` | ✅ Yes | — | Google Gemini API key |
| `DB_PATH` | No | `sustainable_commerce.db` | SQLite database file path |
| `LOG_LEVEL` | No | `INFO` | Logging verbosity |
