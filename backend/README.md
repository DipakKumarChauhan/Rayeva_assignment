# 🚀 AI Sustainable Commerce API

**Role:** Full Stack / AI Intern | **Focus:** Applied AI for Sustainable Commerce

A production-ready Python/FastAPI application implementing AI-powered modules for sustainable B2B commerce using the **Google Gemini API**.

> **Note**: This is the backend API. For full-stack setup instructions, see the [root README](../README.md).

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

## 📁 Project Structure

```
backend/
├── .env.example            # Environment variable template
├── .gitignore             # Git ignore rules
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── architecture.md        # Module 3 & 4 architecture docs
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI entry point & app setup
│   ├── config.py          # Settings, env vars, predefined lists
│   ├── database.py        # SQLite init, connection helpers
│   ├── logger.py          # AI prompt/response logger
│   ├── models/
│   │   ├── __init__.py
│   │   ├── product.py     # Module 1 Pydantic models
│   │   └── proposal.py    # Module 2 Pydantic models
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── catalog.py     # Module 1 API endpoints
│   │   └── proposals.py   # Module 2 API endpoints
│   └── services/
│       ├── __init__.py
│       ├── gemini.py      # Gemini API client wrapper
│       ├── categorizer.py # Module 1 business logic
│       └── proposal_gen.py # Module 2 business logic
└── tests/
    ├── __init__.py
    ├── test_module1.py    # Module 1 tests
    └── test_module2.py    # Module 2 tests
```

---

## 🚀 Quick Start

### 1. Clone & enter the project
```bash
git clone git@github.com:DipakKumarChauhan/Rayeva_assignment.git
cd Rayeva_assignment/backend
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

## 📡 API Reference

### Base URL
```
http://localhost:8000
```

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "ok",
  "service": "AI Sustainable Commerce API",
  "version": "1.0.0"
}
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

## 🧪 Running Tests

```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_module1.py -v
python -m pytest tests/test_module2.py -v

# Run with coverage (if pytest-cov installed)
python -m pytest tests/ --cov=app --cov-report=html
```

**Note**: Tests use mocked Gemini responses — no real API calls needed. All tests are designed to run offline.

---

## 🏗️ Technical Design

### Architecture Principles

| Requirement | Implementation |
|---|---|
| **Structured JSON outputs** | Pydantic models + Gemini JSON-mode prompts with strict validation |
| **Prompt + response logging** | `ai_logs` SQLite table via `app/logger.py` with latency tracking |
| **Environment-based config** | `.env` loaded via `python-dotenv` in `config.py` |
| **Separation of concerns** | `services/` (AI logic) ↔ `routers/` (HTTP) ↔ `models/` (schema) |
| **Error handling** | Pydantic validation + `try/except` → HTTP 500 with detailed messages |
| **JSON extraction** | Robust parsing that handles markdown code fences from AI responses |
| **Database initialization** | Automatic schema creation on startup via `init_db()` |

### Key Components

- **`app/main.py`**: FastAPI app initialization, CORS setup, router registration
- **`app/config.py`**: Centralized configuration with predefined categories and filters
- **`app/database.py`**: SQLite connection management and schema initialization
- **`app/logger.py`**: Context manager for automatic AI call logging
- **`app/services/gemini.py`**: Gemini API wrapper with JSON extraction
- **`app/services/categorizer.py`**: Module 1 business logic with validation
- **`app/services/proposal_gen.py`**: Module 2 business logic with budget constraints

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

## ⚙️ Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `GEMINI_API_KEY` | ✅ Yes | — | Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey)) |
| `DB_PATH` | No | `sustainable_commerce.db` | SQLite database file path |
| `LOG_LEVEL` | No | `INFO` | Logging verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |

### Creating `.env` File

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your Gemini API key:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   DB_PATH=sustainable_commerce.db
   LOG_LEVEL=INFO
   ```

**⚠️ Important**: Never commit `.env` file to version control. It's already in `.gitignore`.

---

## 🔍 Debugging & Logging

### AI Call Logs

All AI interactions are automatically logged to the `ai_logs` table:

```sql
SELECT * FROM ai_logs ORDER BY created_at DESC LIMIT 10;
```

This includes:
- Module name (e.g., `module1_categorizer`, `module2_proposal_gen`)
- Full prompt sent to Gemini
- Complete response received
- Latency in milliseconds
- Timestamp

### Common Issues

**Issue**: `Invalid JSON in AI response`
- **Solution**: The JSON extraction has been improved to handle markdown code fences. If this persists, check the `raw_ai_response` field in the database.

**Issue**: `GEMINI_API_KEY not found`
- **Solution**: Ensure `.env` file exists in the `backend/` directory with your API key.

**Issue**: Database locked errors
- **Solution**: Ensure only one instance of the server is running, or use a different `DB_PATH`.

---

## 📊 Database Management

### Viewing Data

You can use any SQLite client or Python:

```python
import sqlite3

conn = sqlite3.connect('sustainable_commerce.db')
cursor = conn.cursor()

# View all products
cursor.execute("SELECT * FROM products")
print(cursor.fetchall())

# View all proposals
cursor.execute("SELECT * FROM proposals")
print(cursor.fetchall())

# View AI logs
cursor.execute("SELECT module, latency_ms, created_at FROM ai_logs ORDER BY created_at DESC LIMIT 10")
print(cursor.fetchall())

conn.close()
```

### Resetting Database

To start fresh, simply delete the database file:
```bash
rm sustainable_commerce.db
```

The database will be automatically recreated on next server start.

---

## 🔗 Integration with Frontend

The backend is configured with CORS to allow requests from the React frontend:

- **Allowed Origins**: `*` (all origins)
- **Allowed Methods**: All HTTP methods
- **Allowed Headers**: All headers

The frontend should be configured to point to `http://localhost:8000` (or your backend URL).

---

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Google Gemini API Docs](https://ai.google.dev/docs)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

---

## 🎯 Future Enhancements

See [`architecture.md`](./architecture.md) for planned modules:
- **Module 3**: AI Impact Reporting Generator
- **Module 4**: AI WhatsApp Support Bot
