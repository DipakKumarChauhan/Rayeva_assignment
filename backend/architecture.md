# Architecture Documentation — Module 3 & Module 4

> **Note:** Module 1 (AI Auto-Category & Tag Generator) and Module 2 (AI B2B Proposal Generator) are fully implemented. This document outlines the proposed architecture for Module 3 and Module 4.

---

## Module 3: AI Impact Reporting Generator

### Purpose
Automatically generate a human-readable sustainability impact report for each order, estimating:
- Plastic saved (grams)
- Carbon emissions avoided (kg CO₂-equivalent)
- Local sourcing impact
- A comprehensive human-readable impact statement

### Architecture

```
Order Created/Updated
        │
        ▼
┌────────────────────┐
│  Impact Service    │  ◄── Triggered via order webhook or post-checkout hook
│  (impact_gen.py)   │
└────────┬───────────┘
         │  Fetches product sustainability attributes from DB
         ▼
┌────────────────────┐
│  Gemini AI Call    │  ◄── Prompt includes: product list, quantities,
│  (gemini.py)       │       sustainability tags, sourcing data
└────────┬───────────┘
         │
         ▼
┌────────────────────────────────────────────────────────┐
│   Structured JSON Output (stored in `impact_reports`)  │
│   {                                                    │
│     "report_id": "...",                                │
│     "order_id": "...",                                 │
│     "plastic_saved_grams": 150,                        │
│     "carbon_avoided_kg": 2.3,                          │
│     "local_sourcing_percentage": 65,                   │
│     "local_sourcing_summary": "...",                   │
│     "impact_statement": "...",                         │
│     "created_at": "..."                                │
│   }                                                    │
└────────────────────────────────────────────────────────┘
```

### Database Schema

```sql
CREATE TABLE impact_reports (
    report_id                TEXT PRIMARY KEY,
    order_id                 TEXT NOT NULL,
    plastic_saved_grams      REAL,
    carbon_avoided_kg        REAL,
    local_sourcing_percent   REAL,
    local_sourcing_summary   TEXT,
    impact_statement         TEXT NOT NULL,
    raw_ai_response          TEXT,
    created_at               TEXT NOT NULL
);
```

### Gemini Prompt Strategy
- Input: list of products with quantities and sustainability tags
- Calculation context: reference emission factors (e.g., 0.002 kg CO₂/g plastic saved)
- Output format: strict JSON with numeric estimates + text statement
- Model: `gemini-1.5-flash` with temperature 0.2 for deterministic estimates

### API Endpoints
| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/v1/impact/generate` | Generate impact report for an order |
| `GET`  | `/api/v1/impact/{order_id}` | Retrieve impact report by order ID |

---

## Module 4: AI WhatsApp Support Bot

### Purpose
An intelligent WhatsApp chatbot that:
1. Answers order status queries using real database data
2. Handles return policy questions
3. Escalates refund-related issues to a human agent
4. Logs every conversation

### Architecture

```
WhatsApp User Message
        │
        ▼
┌─────────────────────────┐
│  Twilio / Meta Webhook  │  ◄── POST /webhook/whatsapp
│  (webhook_router.py)    │
└──────────┬──────────────┘
           │
           ▼
┌──────────────────────────┐
│  Intent Classifier       │  ◄── Gemini classifies: order_status |
│  (whatsapp_service.py)   │       return_policy | refund | general
└──────────┬───────────────┘
           │
     ┌─────┴──────┐
     │            │
     ▼            ▼
┌──────────┐  ┌──────────────────────┐
│  DB Lookup│  │  Gemini Response Gen │
│(orders,  │  │  (context-aware)     │
│ policies)│  └──────────────────────┘
└────┬─────┘
     │
     ▼
┌────────────────────────────────────┐
│  Escalation Check                  │
│  if refund/high-priority → flag    │
│  human agent via email/Slack       │
└────────────────────────────────────┘
     │
     ▼
┌────────────────────────────────────┐
│  Send WhatsApp Response            │
│  + Log conversation to DB          │
└────────────────────────────────────┘
```

### Database Schema

```sql
CREATE TABLE whatsapp_conversations (
    conversation_id  TEXT PRIMARY KEY,
    phone_number     TEXT NOT NULL,
    message_in       TEXT NOT NULL,
    intent           TEXT,              -- order_status | return_policy | refund | general
    message_out      TEXT NOT NULL,
    escalated        INTEGER DEFAULT 0, -- 1 if escalated
    order_id         TEXT,              -- linked order if applicable
    ai_log_id        TEXT,              -- FK to ai_logs
    created_at       TEXT NOT NULL
);
```

### Intent Routing Logic

| Intent | Action |
|--------|--------|
| `order_status` | Query `orders` table → format response |
| `return_policy` | Retrieve static policy document → AI formats |
| `refund` | Fetch order + flag for escalation → notify human |
| `general` | Gemini generates response from context |

### Gemini Prompt Strategy
- **Step 1 (Classification):** Short prompt → returns one of 4 intent labels in JSON
- **Step 2 (Response Generation):** Full prompt with DB context → natural language reply
- Both steps logged in `ai_logs` table

### External Integrations
- **Twilio API** or **Meta Cloud API** for WhatsApp messaging
- **SendGrid / Slack webhook** for escalation notification
- Environment variables: `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `WHATSAPP_FROM_NUMBER`

### API Endpoints
| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/webhook/whatsapp` | Receive incoming WhatsApp messages |
| `GET`  | `/api/v1/support/conversations` | List all logged conversations |
| `GET`  | `/api/v1/support/conversations/{id}` | Get single conversation |
| `GET`  | `/api/v1/support/escalations` | List escalated tickets |
