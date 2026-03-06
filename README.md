# 🌱 AI Sustainable Commerce Platform

A full-stack AI-powered platform for sustainable B2B commerce, featuring intelligent product categorization and automated proposal generation using Google Gemini AI.

**Video Demo**: [Watch here](https://drive.google.com/file/d/1VGcepij3H3syWTAY9XdXGIiYgApAnzNL/view?usp=sharing)

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.6-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-19.2.0-61DAFB?logo=react)](https://react.dev/)
[![Gemini AI](https://img.shields.io/badge/Gemini-2.5--Flash-4285F4?logo=google)](https://ai.google.dev/)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [API Documentation](#api-documentation)
- [Frontend Usage](#frontend-usage)
- [Testing](#testing)
- [Environment Setup](#environment-setup)
- [Contributing](#contributing)

---

## 🎯 Overview

This platform combines **FastAPI** backend with **React** frontend to deliver two core AI-powered modules:

1. **Module 1: AI Auto-Category & Tag Generator**  
   Automatically categorizes sustainable products with SEO tags and sustainability filters using AI.

2. **Module 2: AI B2B Proposal Generator**  
   Generates comprehensive procurement proposals with product recommendations, budget allocation, and impact summaries.

All AI interactions are powered by **Google Gemini 2.5 Flash** and logged to SQLite for analytics and debugging.

---

## ✨ Features

### Backend (FastAPI)
- ✅ RESTful API with automatic OpenAPI/Swagger documentation
- ✅ AI-powered product categorization with predefined categories
- ✅ Intelligent B2B proposal generation with budget constraints
- ✅ SQLite database with automatic schema initialization
- ✅ Comprehensive AI call logging (prompts, responses, latency)
- ✅ Pydantic models for request/response validation
- ✅ Error handling with detailed error messages
- ✅ CORS enabled for frontend integration

### Frontend (React)
- ✅ Modern dark-themed UI with excellent UX
- ✅ Responsive design (mobile-friendly)
- ✅ Real-time form validation
- ✅ Interactive product categorization interface
- ✅ Comprehensive B2B proposal generation form
- ✅ Session-based history tracking
- ✅ Clean API integration layer
- ✅ Loading states and error handling

---

## 🛠 Tech Stack

### Backend
- **Framework**: FastAPI 0.115.6
- **AI**: Google Gemini 2.5 Flash API
- **Database**: SQLite with sqlite3
- **Validation**: Pydantic 2.10.5
- **Server**: Uvicorn (ASGI)
- **Testing**: Pytest 8.3.5

### Frontend
- **Framework**: React 19.2.0
- **Build Tool**: Vite 7.3.1
- **Language**: JavaScript (JSX)
- **Styling**: CSS3 with modern design patterns
- **HTTP Client**: Native Fetch API

---

## 📁 Project Structure

```
Rayeva_assignment/
├── backend/                    # FastAPI backend application
│   ├── app/
│   │   ├── main.py            # FastAPI entry point
│   │   ├── config.py          # Configuration & settings
│   │   ├── database.py        # SQLite setup & helpers
│   │   ├── logger.py          # AI call logging
│   │   ├── models/            # Pydantic models
│   │   │   ├── product.py     # Module 1 models
│   │   │   └── proposal.py    # Module 2 models
│   │   ├── routers/           # API endpoints
│   │   │   ├── catalog.py     # Module 1 routes
│   │   │   └── proposals.py   # Module 2 routes
│   │   └── services/          # Business logic
│   │       ├── gemini.py      # Gemini API wrapper
│   │       ├── categorizer.py # Module 1 service
│   │       └── proposal_gen.py # Module 2 service
│   ├── tests/                 # Test suite
│   ├── requirements.txt       # Python dependencies
│   ├── README.md             # Backend documentation
│   └── .env.example          # Environment template
│
├── frontend/                   # React frontend application
│   ├── src/
│   │   ├── App.jsx           # Main application component
│   │   ├── App.css           # Application styles
│   │   ├── api.js            # API client layer
│   │   ├── main.jsx          # React entry point
│   │   └── index.css         # Global styles
│   ├── package.json          # Node dependencies
│   └── vite.config.js        # Vite configuration
│
└── README.md                  # This file
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+** (for backend)
- **Node.js 18+** (for frontend)
- **Google Gemini API Key** ([Get one here](https://aistudio.google.com/app/apikey))

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   # venv\Scripts\activate    # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your Gemini API key
   ```
   
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   DB_PATH=sustainable_commerce.db
   LOG_LEVEL=INFO
   ```

5. **Start the server**
   ```bash
   uvicorn app.main:app --reload
   ```

   Backend will be available at: **http://localhost:8000**  
   API Documentation: **http://localhost:8000/docs**

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

   Frontend will be available at: **http://localhost:5173** (or similar)

4. **Configure API URL (optional)**
   
   If your backend runs on a different URL, create `.env` in `frontend/`:
   ```env
   VITE_API_BASE_URL=http://localhost:8000
   ```

---

## 📚 API Documentation

### Module 1: AI Auto-Category & Tag Generator

#### Categorize Product
```http
POST /api/v1/catalog/categorize
Content-Type: application/json

{
  "name": "Bamboo Toothbrush",
  "description": "Eco-friendly bamboo toothbrush with BPA-free soft bristles."
}
```

#### List Products
```http
GET /api/v1/catalog/products
```

#### Get Product
```http
GET /api/v1/catalog/products/{product_id}
```

### Module 2: AI B2B Proposal Generator

#### Generate Proposal
```http
POST /api/v1/proposals/generate
Content-Type: application/json

{
  "company_name": "GreenCorp Solutions",
  "industry": "Corporate Gifting",
  "budget": 50000,
  "preferences": ["plastic-free", "vegan", "recycled"],
  "quantity_needed": 100,
  "use_case": "Employee gifting for Earth Day 2025"
}
```

#### List Proposals
```http
GET /api/v1/proposals/
```

#### Get Proposal
```http
GET /api/v1/proposals/{proposal_id}
```

### Health Check
```http
GET /health
```

**Full API Documentation**: Visit `http://localhost:8000/docs` when the backend is running.

---

## 🎨 Frontend Usage

### Catalog Module
1. Navigate to **"Catalog AI"** tab
2. Enter product name and description
3. Click **"Categorize Product"**
4. View AI-generated categories, SEO tags, and sustainability filters
5. Check **"Recent Runs"** for session history

### B2B Proposals Module
1. Navigate to **"B2B Proposals"** tab
2. Fill in company details:
   - Company name
   - Industry
   - Budget (INR)
   - Quantity needed
   - Sustainability preferences (comma-separated)
   - Use case description
3. Click **"Generate Proposal"**
4. View comprehensive proposal with:
   - Product mix recommendations
   - Budget allocation breakdown
   - Cost breakdown (subtotal, packaging, logistics, fees)
   - Impact summary
5. Check **"Recent Proposals"** for session history

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
source venv/bin/activate
python -m pytest tests/ -v
```

Tests use mocked Gemini responses — no real API calls needed.

### Frontend Linting
```bash
cd frontend
npm run lint
```

---

## ⚙️ Environment Setup

### Backend Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GEMINI_API_KEY` | ✅ Yes | — | Google Gemini API key |
| `DB_PATH` | No | `sustainable_commerce.db` | SQLite database file path |
| `LOG_LEVEL` | No | `INFO` | Logging verbosity |

### Frontend Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `VITE_API_BASE_URL` | No | `http://localhost:8000` | Backend API base URL |

---

## 🗄️ Database Schema

The application uses SQLite with three main tables:

- **`ai_logs`**: Logs all AI API calls (prompt, response, latency)
- **`products`**: Stores categorized products (Module 1)
- **`proposals`**: Stores generated proposals (Module 2)

Database is automatically initialized on first run. See [`backend/README.md`](./backend/README.md) for detailed schema.

---

## 🎯 Key Features & Design Decisions

### AI Integration
- **Robust JSON extraction**: Handles markdown code fences in AI responses
- **Structured prompts**: Clear instructions with constraints for consistent outputs
- **Comprehensive logging**: Every AI call is logged with metadata for debugging

### Backend Architecture
- **Separation of concerns**: Routers → Services → Models
- **Type safety**: Pydantic models for validation
- **Error handling**: Detailed error messages for debugging
- **CORS enabled**: Ready for frontend integration

### Frontend Design
- **Dark theme**: Modern, eye-friendly UI
- **Responsive**: Works on desktop, tablet, and mobile
- **User-friendly**: Clear forms, loading states, error messages
- **Session history**: Track recent operations without backend calls

---

## 📝 Additional Documentation

- **[Backend README](./backend/README.md)**: Detailed backend documentation
- **[Architecture Docs](./backend/architecture.md)**: Module 3 & 4 architecture (future modules)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is part of an assignment submission.

---

## 👤 Author

**Dipak Kumar Chauhan**  
Full Stack / AI Intern | Applied AI for Sustainable Commerce

---

## 🙏 Acknowledgments

- Google Gemini AI for powerful language model capabilities
- FastAPI for the excellent web framework
- React team for the amazing frontend library
- Vite for the blazing-fast build tool

---

**Built with ❤️ for sustainable commerce**
