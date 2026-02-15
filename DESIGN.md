# PMI Design Document

**Version:** 1.0  
**Last Updated:** February 2026  
**Status:** Active Development

---

# Table of Contents

1. [Overview](#overview)
2. [Architecture Philosophy](#architecture-philosophy)
3. [System Architecture](#system-architecture)
4. [Design Decisions](#design-decisions)
5. [Data Generation Strategy](#data-generation-strategy)
6. [Model Architecture](#model-architecture)
7. [Evolution Strategy (V1→V2→V3)](#evolution-strategy-v1v2v3)
8. [API Design](#api-design)
9. [Frontend Architecture](#frontend-architecture)
10. [Production Considerations](#production-considerations)
11. [Trade-offs & Constraints](#trade-offs--constraints)

---

# Overview

## What is PMI?

PMI (Predictive Margin Intelligence) is a **decision intelligence platform** that helps retailers predict the outcome of promotional decisions before execution, with full uncertainty quantification.

### Not This:
❌ A machine learning model  
❌ A business intelligence dashboard  
❌ A synthetic regression experiment

### But This:
✅ A decision intelligence system  
✅ Uncertainty quantification engine  
✅ AI-powered business simulator

---

## Core Design Principle

**"Decision intelligence = Prediction + Uncertainty + Risk + Recommendation + Explanation"**

A single prediction is not intelligence. Intelligence is:
1. What will happen? (prediction)
2. How sure are we? (confidence interval)
3. How risky is this? (risk classification)
4. What should I do? (recommendation)
5. Why this prediction? (explanation)
6. What's a better option? (alternative)

This 6-layer output defines our product.

---

# Architecture Philosophy

## 1. Sequencing Over Stacking

**Principle:** Ship V1 quickly, evolve deliberately.

```
✅ Good: V1 (4 weeks) → V2 (post-hackathon) → V3 (Series A)
❌ Bad: Try to build everything at once → never ship
```

**Why:** Working V1 that ships beats half-built V3 that never launches.

---

## 2. Modular from Day 1

**Principle:** Design for evolution, not just V1.

```python
# Abstract interface
class SimulationEngine(ABC):
    @abstractmethod
    def generate_dataset(self, n_samples: int) -> pd.DataFrame:
        pass

# Swappable implementations
V1FormulaSimulator    # Current
V2AgentSimulator      # Future
V3TemporalSimulator   # Future future
```

**Why:** V1 shouldn't block V2. Plugin architecture enables clean evolution.

---

## 3. Schema-Driven Development

**Principle:** Features are dynamic, not hard-coded.

```python
# Bad (blocks V2):
features = [discount, duration, velocity]  # Fixed list

# Good (enables V2):
schema = simulator.get_feature_schema()
features = self._extract_features(params, schema)
```

**Why:** V2 may add features. Code should adapt automatically.

---

## 4. Uncertainty as First-Class Citizen

**Principle:** Every prediction has uncertainty.

```python
# Not just this:
prediction = model.predict(X)

# But this:
prediction = {
    'point': point_estimate,
    'confidence_interval': (p10, p90),
    'risk': risk_classification,
    'recommendation': business_recommendation
}
```

**Why:** Decisions under uncertainty require risk quantification, not just point estimates.

---

# System Architecture

## High-Level Components

```
┌─────────────────────────────────────────────────┐
│              USER INTERFACE (React)              │
│  Dashboard | Simulator | Alerts | Analytics     │
└──────────────────┬──────────────────────────────┘
                   │ REST API
                   ▼
┌─────────────────────────────────────────────────┐
│            API LAYER (FastAPI)                   │
│  Validation → Prediction → Explanation           │
└──────────────────┬──────────────────────────────┘
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
┌────────────┐ ┌────────┐ ┌──────────┐
│ ML Models  │ │Database│ │Simulator │
│ (3 models) │ │(Postgres)│ (Pluggable)│
└────────────┘ └────────┘ └──────────┘
```

---

## Component Details

### 1. Simulation Engine (Pluggable)

**Purpose:** Generate training data OR simulate decisions at inference.

**V1 Implementation:**
- Correlated feature generation (6 key features)
- 3 non-linear interactions
- Heteroskedastic noise

**Interface:**
```python
class SimulationEngine(ABC):
    def generate_dataset(self, n_samples: int) -> pd.DataFrame
    def simulate_decision(self, params: Dict) -> Dict
    def get_feature_schema(self) -> Dict
```

**Why Pluggable:** V2 will replace formula with agent-based simulation without touching ML/API code.

---

### 2. ML Ensemble (3 Models)

**Purpose:** Multi-model approach for robustness + uncertainty.

**Models:**
1. **Linear Baseline** (Ridge Regression)
   - Purpose: Interpretability
   - Output: Coefficients ("1% discount → -₹2,341")
   - R² Target: 0.65-0.70

2. **XGBoost** (Gradient Boosting)
   - Purpose: Performance
   - Output: Point prediction
   - R² Target: 0.85-0.90

3. **Quantile Regression** (GBM with quantile loss)
   - Purpose: Uncertainty
   - Output: p10, p50, p90
   - Calibration: 80% CI should contain 80% of actuals

**Why 3 Models:** 
- Linear can't be circular (proves learning)
- XGBoost maximizes accuracy
- Quantile provides uncertainty

---

### 3. Prediction Service

**Purpose:** Transform ML outputs into business intelligence.

**6-Layer Output:**

```python
{
    # Layer 1: Prediction
    'prediction': -52340,
    
    # Layer 2: Confidence interval
    'confidence_interval': {
        'lower': -85230,
        'upper': -22110,
        'range': 63120
    },
    
    # Layer 3: Risk classification
    'risk': 'HIGH',  # HIGH/MEDIUM/LOW
    'outcome': 'LIKELY LOSS',
    
    # Layer 4: Recommendation
    'recommendation': 'High uncertainty - recommend A/B test first',
    
    # Layer 5: Explanation
    'explanation': [
        'discount_percent = 30 decreases profit by ₹42,120',
        'return_rate = 0.15 decreases profit by ₹18,430'
    ],
    
    # Layer 6: Alternative
    'alternative': {
        'discount_percent': 20,
        'expected_profit': 18250,
        'risk': 'MEDIUM'
    }
}
```

---

### 4. Explainability Layer

**Purpose:** Make predictions interpretable.

**Approach:** SHAP (SHapley Additive exPlanations)

**Outputs:**
- **Global:** Top 5 features by importance
- **Local:** Top 3 drivers for this prediction
- **Format:** Business language, not ML jargon

**Example:**
```
Global: "discount_percent is the #1 profit driver"
Local: "discount=30% decreases YOUR profit by ₹42,120"
```

---

### 5. Input Validation

**Purpose:** Prevent garbage predictions.

**Validation Layers:**
1. **Range checks** (discount: 0-80%, duration: 1-60 days)
2. **Business logic** (inventory < expected sales → warning)
3. **Extrapolation detection** (outside training domain → warning)

**Philosophy:** Fail fast with clear messages, not silent wrong predictions.

---

# Design Decisions

## Decision 1: Why Correlated Features?

**Problem:** Independent features → model just memorizes formula.

**Solution:** Correlation matrix ensuring realistic relationships:
- discount ↔ velocity (0.65 correlation)
- returns ↔ support (0.55 correlation)
- price ↔ velocity (-0.60 correlation)

**Proof of Learning:** Linear R² < 0.70 shows model can't reverse-engineer formula.

---

## Decision 2: Why 3 Models, Not 1?

**Option A (Rejected):** Single XGBoost model
- ✅ Pro: Simple
- ❌ Con: No interpretability
- ❌ Con: No uncertainty
- ❌ Con: Looks like typical ML

**Option B (Chosen):** 3-model ensemble
- ✅ Pro: Interpretability (Linear)
- ✅ Pro: Accuracy (XGBoost)
- ✅ Pro: Uncertainty (Quantile)
- ✅ Pro: Shows rigor
- ❌ Con: More complex

**Why Chosen:** The 3 models serve different purposes, not redundancy.

---

## Decision 3: Why Quantile Regression for Uncertainty?

**Alternatives Considered:**

1. **Monte Carlo Simulation** (1000 runs)
   - ❌ Too slow for real-time (2+ seconds)
   - ❌ Overkill for V1

2. **Bayesian Neural Network**
   - ❌ Hard to explain
   - ❌ Longer training time
   - ❌ No accuracy advantage

3. **Quantile Regression** ✅
   - ✅ Fast inference (<100ms)
   - ✅ Standard approach
   - ✅ Easy to explain ("10th to 90th percentile")
   - ✅ Calibrated uncertainty

**Decision:** Quantile regression is the pragmatic choice for V1.

---

## Decision 4: Why Plugin Architecture for Simulator?

**Problem:** V1 uses formula, V2 will use agent simulation.

**Bad Approach:** 
```python
# V1 code
profit = calculate_formula(params)

# V2 rewrite
profit = simulate_agents(params)  # Breaks everything
```

**Good Approach:**
```python
# V1 and V2 use same interface
simulator = Config.get_simulator()  # Returns V1 or V2
profit = simulator.simulate_decision(params)  # Same call
```

**Why:** Clean V1→V2 transition without breaking ML/API code.

---

## Decision 5: Why 6-Layer Output?

**The ML Demo Output:**
```json
{"prediction": -52340}
```

**The Decision Intelligence Output:**
```json
{
  "prediction": -52340,
  "confidence_interval": {"lower": -85230, "upper": -22110},
  "risk": "HIGH",
  "recommendation": "Recommend A/B test first",
  "explanation": ["discount decreases profit by ₹42k"],
  "alternative": {"discount": 20, "profit": 18250}
}
```

**Why 6 Layers:** Because retailers need to make decisions, not just see predictions.

---

# Data Generation Strategy

## V1: Realistic Formula Simulator

### Approach

**Not:** Simple deterministic formula
**But:** Correlated features + interactions + heteroskedastic noise

### Components

1. **Correlation Matrix** (6 key features)
2. **Non-linear Interactions** (3 key patterns)
3. **Heteroskedastic Noise** (variance depends on conditions)

### Proof of Non-Circularity

**Test:** Train Linear Regression on generated data.

**Expected Result:** R² < 0.70

**Why:** If Linear R² > 0.80, model is just memorizing formula. If R² < 0.70, model must discover patterns.

**V1 Target:** Linear R² = 0.68 ✅

---

## V2: Agent-Based Simulator (Future)

### Approach

Replace formula with multi-agent market simulation:
- Customer agents respond to price
- Competitor agents respond to our moves
- Inventory system enforces constraints
- Market conditions affect all agents

### Emergent Properties

Outcomes emerge from agent interactions, not pre-programmed formulas:
- Price wars emerge when all competitors discount
- Stockouts kill momentum (not formula, but constraint)
- Word-of-mouth boosts (network effect, not calculation)

**Why Later:** Takes 40+ hours. V1 proves concept first.

---

# Model Architecture

## Training Pipeline

```
Data Generation (Simulator)
  ↓
Feature Engineering (encode categoricals)
  ↓
Train-Val-Test Split (60-20-20)
  ↓
Train 3 Models in Parallel
  ├─ Linear (Ridge with α=10)
  ├─ XGBoost (hyperparameter tuning)
  └─ Quantile (3 models: p10, p50, p90)
  ↓
Model Comparison & Selection
  ↓
Save Models + Metadata
```

## Inference Pipeline

```
User Input
  ↓
Input Validation (ranges, business logic)
  ↓
Feature Preparation (match training schema)
  ↓
Predict with 3 Models
  ├─ XGBoost → point prediction
  ├─ Quantile → confidence interval
  └─ Linear → coefficients (for explanation)
  ↓
Risk Classification (HIGH/MEDIUM/LOW)
  ↓
Generate Recommendation
  ↓
SHAP Explanation (top 3 drivers)
  ↓
Generate Alternative
  ↓
Return 6-Layer Output
```

---

# Evolution Strategy (V1→V2→V3)

## V1: Hackathon MVP (Current)

**Scope:** 5 components, 4 weeks

**Components:**
1. Correlated data generation
2. Multi-model ensemble (Linear, XGBoost, Quantile)
3. Uncertainty quantification
4. SHAP explainability
5. Input validation

**Success Criteria:**
- ✅ Linear R² < 0.70 (non-circular)
- ✅ XGBoost R² > 0.80 (accurate)
- ✅ 6-layer output working
- ✅ Judges say "this could work in production"

**Timeline:** 4 weeks

---

## V2: Agent-Based Simulation (Post-Hackathon)

**Scope:** Replace simulator core

**Changes:**
1. Replace `V1FormulaSimulator` with `V2AgentSimulator`
2. Add multi-agent market dynamics
3. Integrate real retailer data
4. Retrain models on emergent data

**What Stays Same:**
- ML training pipeline (uses same interface)
- API endpoints (same 6-layer output)
- Frontend (no changes needed)

**Success Criteria:**
- ✅ Simulation produces more realistic patterns
- ✅ Model R² maintained or improved
- ✅ Pilot with 1-3 retailers

**Timeline:** 8-12 weeks

---

## V3: Temporal Intelligence (Series A)

**Scope:** Add time dimension

**Changes:**
1. Replace `V2AgentSimulator` with `V3TemporalSimulator`
2. Add sequential decision effects
3. Track brand equity over time
4. Model customer memory

**New Features:**
- Sequential optimization ("If you discount now, what happens next month?")
- Brand equity tracking
- Customer habituation modeling
- Strategic scenario planning

**Success Criteria:**
- ✅ Can model multi-period effects
- ✅ Enterprise clients
- ✅ Series A raise

**Timeline:** 6 months

---

## Why This Phasing Works

**V1→V2:** Same interface, swap implementation
```python
# V1
simulator = V1FormulaSimulator()

# V2 (just change config)
simulator = V2AgentSimulator()  # Everything else works
```

**V2→V3:** Same pattern
```python
simulator = V3TemporalSimulator()  # Inherits from V2
```

**Key Insight:** Plugin architecture means V1 doesn't block V2, V2 doesn't block V3.

---

# API Design

## REST API Principles

1. **Resource-based URLs** (`/api/v1/products`, not `/api/v1/getProducts`)
2. **Consistent response format** (always JSON, always same structure)
3. **Versioned** (`/api/v1/` allows future `/api/v2/`)
4. **Well-documented** (Swagger/OpenAPI auto-generated)

## Key Endpoints

### POST /api/v1/simulate/decision

**Purpose:** Main prediction endpoint

**Request:**
```json
{
  "discount_percent": 30,
  "duration_days": 14,
  "category": "electronics",
  "price": 29999
}
```

**Response:**
```json
{
  "prediction": -52340,
  "confidence_interval": {"lower": -85230, "upper": -22110},
  "risk": "HIGH",
  "recommendation": "Recommend A/B test first",
  "explanation": [...],
  "alternative": {...}
}
```

### GET /api/v1/products

**Purpose:** List products with margin data

### GET /api/v1/products/{id}/costs

**Purpose:** Hidden cost breakdown for product

---

# Frontend Architecture

## Tech Stack

- **Framework:** React 18.2 with Vite
- **Routing:** React Router v6
- **State:** React Query (server) + Zustand (client)
- **Styling:** Tailwind CSS
- **Charts:** Recharts

## Component Structure

```
src/
├── pages/
│   ├── Dashboard.jsx       # Overview + products
│   ├── Simulator.jsx       # Decision simulation
│   └── Alerts.jsx          # Alert center
├── components/
│   ├── ProductCard.jsx     # Reusable card
│   ├── charts/
│   │   └── CostBreakdown.jsx
│   └── common/
│       ├── LoadingSpinner.jsx
│       └── ErrorMessage.jsx
├── api/
│   └── client.js           # API wrapper
└── App.jsx
```

## Design Principles

1. **API-first:** Frontend is thin client, all logic in backend
2. **Responsive:** Works on desktop, tablet, mobile
3. **Loading states:** Always show loading/error states
4. **Real-time validation:** Validate inputs before API call

---

# Production Considerations

## Performance

**Target:** <500ms end-to-end prediction

**Bottlenecks:**
- ML inference: ~150ms (XGBoost + Quantile)
- SHAP explanation: ~100ms
- Database query: ~50ms
- Network: ~100ms

**Optimizations:**
- Model loading: Load once at startup, not per request
- SHAP caching: Cache explainer object
- Database indexing: Index on product_id, category

---

## Monitoring

**Metrics to Track:**
- Prediction latency (p50, p95, p99)
- Model accuracy over time (MAE drift)
- API error rate
- User engagement (predictions per day)

**Alerts:**
- Latency > 1 second
- MAE degradation > 20%
- Error rate > 1%

---

## Security

**Input Validation:**
- Range checks on all numeric inputs
- Sanitize all string inputs
- Rate limiting (100 req/min per user)

**API Security:**
- HTTPS only in production
- CORS configured for known origins
- JWT authentication (future)

---

# Trade-offs & Constraints

## What We Chose

### ✅ Multi-Model Ensemble
**Trade-off:** Complexity vs. robustness  
**Choice:** 3 models (worth the complexity)  
**Why:** Interpretability + accuracy + uncertainty all matter

### ✅ Quantile Regression
**Trade-off:** Speed vs. uncertainty quality  
**Choice:** Quantile (fast, good enough)  
**Why:** Monte Carlo too slow for V1

### ✅ Correlated Features
**Trade-off:** Generation complexity vs. realism  
**Choice:** Correlation matrix (2 hours extra)  
**Why:** Prevents circular learning

### ✅ Plugin Architecture
**Trade-off:** Upfront design vs. evolution ease  
**Choice:** Plugin pattern (2 hours extra)  
**Why:** Clean V1→V2→V3 path

---

## What We Deferred

### ❌ Full Agent Simulation
**Deferred to:** V2  
**Why:** 40+ hours, not demo-able in 8 minutes

### ❌ Temporal Dynamics
**Deferred to:** V3  
**Why:** Complex, sequential decisions hard to demo

### ❌ Drift Detection
**Deferred to:** Post-launch  
**Why:** Production concern, not demo concern

### ❌ A/B Testing Framework
**Deferred to:** Post-pilot  
**Why:** Needs real users first

---

## Constraints

### Time Constraint
**4 weeks to V1** → Focus on 6-layer output, not simulation complexity

### Team Constraint
**3 people** → Modular architecture so we don't block each other

### Demo Constraint
**8 minutes** → Every feature must be demo-able or it doesn't exist

### Credibility Constraint
**Must look beyond typical ML** → Hence 6-layer output, multi-model, uncertainty

---

# Success Metrics

## V1 Success

**Technical:**
- ✅ Linear R² < 0.70 (proves learning)
- ✅ XGBoost R² > 0.80 (proves accuracy)
- ✅ Latency < 500ms (proves production-ready)

**Business:**
- ✅ Judges say "this could work in production"
- ✅ Retailers interested in pilot
- ✅ Clear V1→V2→V3 path

**Product:**
- ✅ 6-layer output complete
- ✅ Explainability clear
- ✅ Uncertainty quantified

---

# Conclusion

PMI V1 is a **minimal credible decision intelligence system** designed for:
1. **Hackathon success** (4-week timeline)
2. **Evolution capability** (V1→V2→V3 clean path)
3. **Production credibility** (not just academic)

**Key Architectural Decisions:**
- Plugin pattern for simulator (enables evolution)
- Multi-model ensemble (interpretability + accuracy + uncertainty)
- 6-layer output (decision intelligence, not just ML)
- Schema-driven (adapts to V2 features automatically)

**The Result:** A working V1 that can evolve into V2 agent simulation and V3 temporal intelligence without architectural rewrites.

---

**Document Version:** 1.0  
**Last Updated:** February 2026  
**Next Review:** Post-V1 launch
