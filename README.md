# PMI - Predictive Margin Intelligence

Key Documentation:
- DESIGN.md
- REQUIREMENTS.md

<div align="center">

**AI-Powered Decision Intelligence for Retail Margin Optimization**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Node 20+](https://img.shields.io/badge/node-20+-green.svg)](https://nodejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688.svg)](https://fastapi.tiangolo.com)
[![React 18](https://img.shields.io/badge/React-18.2-61DAFB.svg)](https://reactjs.org/)

[Features](#-features) • [Quick Start](#-quick-start) • [Architecture](#-architecture) • [Demo](#-demo) • [Documentation](#-documentation)

</div>

---

## 🎯 Problem Statement

**Retailers lose ₹5.4 crore/month to hidden costs in promotional decisions.**

Traditional BI tools show *what happened* (backward-looking analytics), but PMI predicts *what will happen* (forward-looking intelligence) with full uncertainty quantification.

### The Gap:
- **Stated Margin:** 45% (what accounting shows)
- **True Margin:** 12% (after returns, holding, support costs)
- **Hidden Gap:** 33% (₹millions in losses)

PMI helps retailers **predict decision outcomes before execution** using AI.

---

## ✨ Features

### 🤖 Decision Intelligence (Not Just ML)

PMI provides **6-layer intelligence** for every decision:

1. **Prediction**: "Profit: ₹-52,340"
2. **Confidence Interval**: "80% CI: ₹-85k to ₹-22k"
3. **Risk Classification**: "Risk: HIGH"
4. **Business Recommendation**: "Recommend A/B test on 10% inventory first"
5. **Explanation**: "Top driver: discount (-₹42k impact)"
6. **Alternative**: "Try 20% discount → +₹18k profit (Risk: MEDIUM)"

### 🎓 Multi-Model Ensemble

- **Linear Baseline**: Interpretability + business coefficients
- **XGBoost**: 87% accuracy + feature importance
- **Quantile Regression**: Uncertainty quantification (p10, p50, p90)

### 🔍 Explainability

- **SHAP Analysis**: Global feature importance + local explanations
- **Top Drivers**: "discount_percent decreases profit by ₹42,120"

### ⚡ Production-Ready

- **Input Validation**: Range checks + business logic
- **Fast Inference**: <500ms predictions
- **API-First**: REST API with Swagger docs

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL 15+ (or use Railway)

### Installation

```bash
# Clone repository
git clone https://github.com/your-team/pmi-project.git
cd pmi-project

# Backend setup
cd backend
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Generate datasets & train models
python scripts/generate_datasets.py
python scripts/train_models.py

# Start backend
uvicorn main:app --reload

# Frontend setup (new terminal)
cd frontend
npm install
npm run dev
```

### Access

- **Frontend**: http://localhost:5173
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────┐
│                  USER INTERFACE                      │
│       "30% off for 14 days on electronics?"         │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│            INPUT VALIDATION LAYER                    │
│  • Range checks • Business logic warnings           │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│       MULTI-MODEL PREDICTION ENSEMBLE                │
│  Linear → XGBoost → Quantile Regression             │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│        DECISION INTELLIGENCE OUTPUT                  │
│  Prediction + Uncertainty + Risk + Explanation      │
└─────────────────────────────────────────────────────┘
```

See [DESIGN.md](DESIGN.md) for detailed architecture.

---

## 🎯 Usage Example

### Via API

```bash
curl -X POST "http://localhost:8000/api/v1/simulate/decision" \
  -H "Content-Type: application/json" \
  -d '{
    "discount_percent": 30,
    "duration_days": 14,
    "category": "electronics"
  }'
```

**Response:**

```json
{
  "prediction": -52340,
  "confidence_interval": {
    "lower": -85230,
    "upper": -22110
  },
  "risk": "HIGH",
  "recommendation": "Recommend A/B test on 10% of inventory first",
  "explanation": [
    "discount_percent = 30.00 decreases profit by ₹42,120"
  ]
}
```

---

## 🧪 Model Performance

| Model | MAE (₹) | R² | MAPE (%) |
|-------|---------|-----|----------|
| Linear | 8,234 | 0.68 | 15.2 |
| XGBoost | 4,187 | 0.87 | 8.3 |
| Quantile | 4,523 | 0.85 | 9.1 |

**Key:** Linear R² < 0.70 proves model learns patterns (not formulas)

---

## 📁 Project Structure

```
pmi-project/
├── backend/
│   ├── api/              # ML & prediction services
│   ├── database/         # Models & data loading
│   ├── ml/               # Model training & explanation
│   ├── routers/          # API endpoints
│   ├── simulation/       # Data generation engine
│   └── main.py           # FastAPI app
├── frontend/
│   ├── src/
│   │   ├── pages/        # Dashboard, Simulator
│   │   └── components/   # UI components
│   └── package.json
├── docs/                 # Documentation
├── models/               # Trained models
└── README.md
```

---

## 🔄 Roadmap

### V1 (Current) - Hackathon MVP ✅
- Correlated data generation
- Multi-model ensemble
- Uncertainty quantification
- 6-layer intelligence output

### V2 (Post-Hackathon) - Agent-Based
- Multi-agent market simulation
- Real retailer data integration

### V3 (Series A) - Strategic Intelligence
- Temporal dynamics
- A/B testing framework

---

## 📚 Documentation

- **[DESIGN.md](DESIGN.md)**: Architecture & design decisions
- **[docs/API_REFERENCE.md](docs/API_REFERENCE.md)**: API documentation
- **[docs/ML_MODELS.md](docs/ML_MODELS.md)**: Model details

---

## 🐳 Docker Deployment

```bash
docker-compose up -d
```

---

## 👥 Team

- **Tanmay** - ML Engineer & Architect
- **Shiv** - Backend & Database
- **Akash** - Frontend & UI/UX

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file.

---

<div align="center">

**Built with ❤️ for better retail decisions**

</div>
