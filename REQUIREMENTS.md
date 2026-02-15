# PMI System Requirements

**Version:** 1.0  
**Last Updated:** February 2026  
**For:** PMI V1 - Decision Intelligence Platform

---

# Table of Contents

1. [System Requirements](#system-requirements)
2. [Backend Dependencies](#backend-dependencies)
3. [Frontend Dependencies](#frontend-dependencies)
4. [Database Requirements](#database-requirements)
5. [Development Tools](#development-tools)
6. [Installation Guide](#installation-guide)
7. [Verification](#verification)
8. [Troubleshooting](#troubleshooting)

---

# System Requirements

## Minimum Hardware

```
CPU:     4 cores (Intel i5 / AMD Ryzen 5 or better)
RAM:     8 GB (16 GB recommended)
Storage: 10 GB free space
         - 2 GB for dependencies
         - 5 GB for models and data
         - 3 GB for Docker images (if using Docker)
```

## Operating Systems

| OS | Version | Status | Notes |
|---|---|---|---|
| **macOS** | 12.0+ (Monterey or later) | ✅ Recommended | Native development environment |
| **Ubuntu** | 20.04 LTS or later | ✅ Recommended | Production deployment target |
| **Windows** | 10/11 with WSL2 | ✅ Supported | Use WSL2, not native Windows |
| **Debian** | 11+ | ✅ Supported | Server deployment |

---

# Backend Dependencies

## Python Environment

### Python Version
```
Required: Python 3.11+
Recommended: Python 3.11.7

Check version:
$ python --version
Python 3.11.7
```

### Why Python 3.11?
- Match expressions (better pattern matching)
- Better error messages
- 10-60% faster than Python 3.10
- Type hinting improvements

---

## Core Backend Dependencies

### File: `backend/requirements.txt`

```txt
# =============================================================================
# WEB FRAMEWORK & SERVER
# =============================================================================
fastapi==0.104.1              # Modern async web framework
uvicorn[standard]==0.24.0     # ASGI server with auto-reload
pydantic==2.5.0               # Data validation using Python type hints
pydantic-settings==2.1.0      # Settings management
python-multipart==0.0.6       # Form data parsing

# =============================================================================
# DATABASE & ORM
# =============================================================================
sqlalchemy==2.0.23            # SQL toolkit and Object-Relational Mapping
alembic==1.13.0               # Database migration tool
psycopg2-binary==2.9.9        # PostgreSQL adapter (binary distribution)
asyncpg==0.29.0               # Async PostgreSQL driver

# =============================================================================
# CACHING & PERFORMANCE
# =============================================================================
redis==5.0.1                  # Redis client for caching
hiredis==2.2.3                # C parser for Redis protocol (faster)

# =============================================================================
# MACHINE LEARNING - CORE
# =============================================================================
numpy==1.26.2                 # Numerical computing foundation
pandas==2.1.3                 # Data manipulation and analysis
scikit-learn==1.3.2           # ML algorithms (Linear, RF, Quantile)
xgboost==2.0.3                # Gradient boosting (primary model)
scipy==1.11.4                 # Scientific computing utilities

# =============================================================================
# MACHINE LEARNING - MODEL MANAGEMENT
# =============================================================================
joblib==1.3.2                 # Model serialization and persistence
shap==0.44.0                  # SHAP values for explainability

# =============================================================================
# SECURITY & AUTHENTICATION
# =============================================================================
python-jose[cryptography]==3.3.0  # JWT token handling
passlib[bcrypt]==1.7.4             # Password hashing
bcrypt==4.1.1                      # Bcrypt algorithm

# =============================================================================
# UTILITIES & HELPERS
# =============================================================================
python-dotenv==1.0.0          # Load environment variables from .env
httpx==0.25.2                 # Async HTTP client
aiofiles==23.2.1              # Async file operations
email-validator==2.1.0        # Email validation
phonenumbers==8.13.26         # Phone number validation

# =============================================================================
# TESTING & QUALITY
# =============================================================================
pytest==7.4.3                 # Testing framework
pytest-asyncio==0.21.1        # Async test support
pytest-cov==4.1.0             # Code coverage reporting
faker==20.1.0                 # Fake data generation for tests
httpx==0.25.2                 # HTTP client for testing APIs

# =============================================================================
# CODE QUALITY & FORMATTING
# =============================================================================
black==23.12.0                # Code formatter (PEP 8 compliant)
flake8==6.1.0                 # Linting (style guide enforcement)
isort==5.13.2                 # Import statement organizer
mypy==1.7.1                   # Static type checker
pylint==3.0.3                 # Code analysis

# =============================================================================
# MONITORING & LOGGING
# =============================================================================
prometheus-client==0.19.0     # Prometheus metrics
python-json-logger==2.0.7     # Structured JSON logging

# =============================================================================
# DEVELOPMENT TOOLS
# =============================================================================
ipython==8.18.1               # Enhanced Python shell
```

---

## Dependency Categories Explained

### Why FastAPI?
- **Performance**: 2-3x faster than Flask/Django
- **Modern**: Async/await support, automatic OpenAPI docs
- **Type Safety**: Leverages Pydantic for validation
- **Developer Experience**: Auto-generated Swagger UI

### Why XGBoost + scikit-learn?
- **XGBoost**: Industry standard for tabular data (Kaggle winner)
- **scikit-learn**: Linear baseline + Quantile regression
- **Compatibility**: Both work seamlessly together

### Why SHAP?
- **Industry Standard**: Used by Microsoft, Google, Amazon
- **Model Agnostic**: Works with any ML model
- **Interpretable**: Business-friendly explanations

### Why PostgreSQL?
- **Reliability**: ACID compliance, proven at scale
- **Features**: JSON support, full-text search
- **Cost**: Free, open-source

---

# Frontend Dependencies

## Node.js Environment

### Node.js Version
```
Required: Node.js 18+
Recommended: Node.js 20.10.0 LTS

Check version:
$ node --version
v20.10.0

$ npm --version
10.2.3
```

---

## Core Frontend Dependencies

### File: `frontend/package.json`

```json
{
  "name": "pmi-frontend",
  "private": true,
  "version": "1.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "lint": "eslint . --ext js,jsx",
    "format": "prettier --write \"src/**/*.{js,jsx,json,css}\"",
    "test": "vitest"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.20.1",
    "@tanstack/react-query": "^5.12.2",
    "zustand": "^4.4.7",
    "axios": "^1.6.2",
    "recharts": "^2.10.3",
    "lucide-react": "^0.294.0",
    "react-hook-form": "^7.48.2",
    "zod": "^3.22.4",
    "date-fns": "^2.30.0",
    "clsx": "^2.0.0",
    "tailwind-merge": "^2.1.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@vitejs/plugin-react": "^4.2.1",
    "vite": "^5.0.8",
    "tailwindcss": "^3.3.6",
    "postcss": "^8.4.32",
    "autoprefixer": "^10.4.16",
    "eslint": "^8.55.0",
    "eslint-plugin-react": "^7.33.2",
    "eslint-plugin-react-hooks": "^4.6.0",
    "prettier": "^3.1.1",
    "prettier-plugin-tailwindcss": "^0.5.9",
    "vitest": "^1.0.4"
  }
}
```

---

## Frontend Dependencies Explained

### Core Framework
- **React 18.2**: Industry standard, huge ecosystem
- **Vite 5**: 10x faster than webpack, hot module replacement
- **React Router v6**: Client-side routing

### State Management
- **@tanstack/react-query**: Server state management
- **Zustand**: Simple client state (lighter than Redux)

### UI & Styling
- **Tailwind CSS**: Utility-first CSS framework
- **lucide-react**: Icon library (500+ icons)
- **Recharts**: Charts built on D3 (simpler API)

### Forms & Validation
- **react-hook-form**: Performant form handling
- **zod**: TypeScript-first schema validation

### HTTP Client
- **axios**: Better than fetch (interceptors, automatic JSON)

### Development
- **ESLint**: Linting
- **Prettier**: Code formatting
- **Vitest**: Testing (faster than Jest)

---

# Database Requirements

## PostgreSQL

### Version
```
Required: PostgreSQL 15+
Recommended: PostgreSQL 15.5

Check version:
$ psql --version
psql (PostgreSQL) 15.5
```

### Required Extensions
```sql
-- UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Fuzzy text search
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Better indexing
CREATE EXTENSION IF NOT EXISTS "btree_gin";
```

### Resource Requirements
```
Connections: 100 concurrent
Memory: 2 GB RAM minimum
Storage: 5 GB minimum
```

---

## Redis (Optional but Recommended)

### Version
```
Required: Redis 7.0+
Recommended: Redis 7.2.3

Check version:
$ redis-cli --version
redis-cli 7.2.3
```

### Purpose
- API response caching
- Session storage
- Rate limiting

### Resource Requirements
```
Memory: 512 MB minimum
Persistence: AOF (Append Only File) recommended
```

---

# Development Tools

## Required Tools

### Git
```
Version: 2.30+
Check: git --version
```

### Code Editor (Choose One)

**Recommended: VS Code**
```
Version: 1.85+
Extensions:
- Python (ms-python.python)
- Pylance (ms-python.vscode-pylance)
- ESLint (dbaeumer.vscode-eslint)
- Prettier (esbenp.prettier-vscode)
- Tailwind CSS IntelliSense (bradlc.vscode-tailwindcss)
```

**Alternative: PyCharm**
```
Version: 2023.3+
Professional Edition recommended (free for students)
```

---

## Optional Tools

### Docker & Docker Compose
```
Docker: 20.10+
Docker Compose: 2.0+

Purpose: Containerized development & deployment
```

### Postman / Insomnia
```
Purpose: API testing
Alternative: Thunder Client (VS Code extension)
```

---

# Installation Guide

## Step 1: System Prerequisites

### macOS
```bash
# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.11
brew install python@3.11

# Install Node.js 20
brew install node@20

# Install PostgreSQL
brew install postgresql@15
brew services start postgresql@15

# Install Redis (optional)
brew install redis
brew services start redis

# Install Git
brew install git
```

### Ubuntu/Debian
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip -y

# Install Node.js 20
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install nodejs -y

# Install PostgreSQL
sudo apt install postgresql-15 postgresql-contrib -y
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Install Redis
sudo apt install redis-server -y
sudo systemctl start redis-server
sudo systemctl enable redis-server

# Install Git
sudo apt install git -y
```

### Windows (WSL2)
```powershell
# Install WSL2
wsl --install

# Then follow Ubuntu instructions inside WSL
```

---

## Step 2: Project Setup

### Clone Repository
```bash
git clone https://github.com/your-team/pmi-project.git
cd pmi-project
```

---

## Step 3: Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows (WSL):
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your settings

# Setup database
createdb pmi_db
createuser pmi_user -P

# Run migrations
alembic upgrade head

# Generate datasets
python scripts/generate_datasets.py

# Train models
python scripts/train_models.py

# Start server
uvicorn main:app --reload
```

---

## Step 4: Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create .env file
cp .env.example .env
# Edit .env with your settings

# Run development server
npm run dev
```

---

## Step 5: Verification

### Backend Verification
```bash
# Server should be running
curl http://localhost:8000/health
# Expected: {"status": "healthy"}

# Check API docs
open http://localhost:8000/docs
```

### Frontend Verification
```bash
# App should be running
open http://localhost:5173
```

### Database Verification
```bash
psql -U pmi_user -d pmi_db -c "SELECT COUNT(*) FROM products;"
# Expected: 500
```

---

# Environment Variables

## Backend (.env)

```bash
# Application
APP_NAME=PMI
ENVIRONMENT=development
DEBUG=True

# Server
HOST=0.0.0.0
PORT=8000

# Database
DATABASE_URL=postgresql://pmi_user:password@localhost:5432/pmi_db

# Redis (optional)
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256

# CORS
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# ML Models
MODEL_PATH=models/
```

## Frontend (.env)

```bash
# API Configuration
VITE_API_BASE_URL=http://localhost:8000
VITE_API_TIMEOUT=30000

# Application
VITE_APP_NAME=PMI
VITE_APP_VERSION=1.0.0

# Environment
VITE_ENVIRONMENT=development
```

---

# Verification

## Complete System Check

```bash
# Backend health
curl http://localhost:8000/health
# ✅ {"status": "healthy"}

# API documentation
curl http://localhost:8000/openapi.json | jq '.info'
# ✅ {"title": "PMI API", "version": "1.0.0"}

# Database connection
psql $DATABASE_URL -c "SELECT version();"
# ✅ PostgreSQL version info

# Redis connection (if using)
redis-cli ping
# ✅ PONG

# Frontend build
cd frontend && npm run build
# ✅ dist/ folder created

# Python packages
pip list | grep -E "fastapi|xgboost|shap"
# ✅ All packages listed

# Node packages
npm list --depth=0 | grep -E "react|vite"
# ✅ All packages listed

# Models exist
ls -lh backend/models/
# ✅ margin_predictor.pkl, quantile_models.pkl

# Data generated
ls -lh backend/data/
# ✅ pmi_v1_dataset.csv (3000 rows)
```

---

# Troubleshooting

## Common Issues

### Issue: Python version wrong
```bash
# Check current version
python --version

# Install pyenv for version management
curl https://pyenv.run | bash

# Install Python 3.11
pyenv install 3.11.7
pyenv global 3.11.7

# Verify
python --version  # Should show 3.11.7
```

### Issue: PostgreSQL connection refused
```bash
# Check if running
# macOS:
brew services list | grep postgresql

# Ubuntu:
sudo systemctl status postgresql

# Start if stopped
brew services start postgresql@15  # macOS
sudo systemctl start postgresql    # Ubuntu

# Test connection
psql -U postgres -c "SELECT version();"
```

### Issue: Redis connection refused
```bash
# Start Redis
brew services start redis  # macOS
sudo systemctl start redis-server  # Ubuntu

# Test connection
redis-cli ping  # Should return PONG
```

### Issue: Port already in use
```bash
# Find process using port 8000
lsof -i :8000

# Kill process
kill -9 <PID>

# Or use different port
uvicorn main:app --port 8001
```

### Issue: npm install fails
```bash
# Clear cache
npm cache clean --force

# Delete lock file and node_modules
rm -rf node_modules package-lock.json

# Reinstall
npm install
```

### Issue: Models not training
```bash
# Check dataset exists
ls -lh backend/data/pmi_v1_dataset.csv

# Check Python packages
pip list | grep -E "xgboost|scikit-learn"

# Re-run generation
python scripts/generate_datasets.py

# Re-run training with verbose output
python scripts/train_models.py --verbose
```

### Issue: SHAP installation fails on Apple Silicon
```bash
# Install with conda (easier for M1/M2 Macs)
conda install -c conda-forge shap

# Or use pip with specific build
pip install shap --no-binary shap
```

---

# Platform-Specific Notes

## macOS (Apple Silicon M1/M2/M3)

### Special Considerations
```bash
# Some packages need Rosetta 2
softwareupdate --install-rosetta

# Use conda for ML packages (recommended)
brew install miniforge
conda create -n pmi python=3.11
conda activate pmi
conda install numpy pandas scikit-learn xgboost

# Or use pip with arch flags
arch -arm64 pip install xgboost
```

## Windows (WSL2)

### Performance Tips
```bash
# Store project in WSL filesystem (not /mnt/c/)
cd ~
git clone https://github.com/your-team/pmi-project.git

# Access from Windows
# In File Explorer: \\wsl$\Ubuntu\home\username\pmi-project
```

## Ubuntu Server (Production)

### Additional Security
```bash
# Setup firewall
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable

# Create non-root user
sudo adduser pmi
sudo usermod -aG sudo pmi
```

---

# Docker Alternative

If you prefer Docker (simplifies setup):

```bash
# Start all services
docker-compose up -d

# Access
# Frontend: http://localhost:80
# Backend: http://localhost:8000
# PostgreSQL: localhost:5432
# Redis: localhost:6379

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

---

# Minimum vs Recommended

## Minimum (Will Work)
- Python 3.11, Node 18
- 8 GB RAM
- PostgreSQL 15
- No Redis
- SQLite for development

## Recommended (Better Performance)
- Python 3.11.7, Node 20 LTS
- 16 GB RAM
- PostgreSQL 15.5
- Redis 7.2
- SSD storage

## Production (Best Experience)
- Python 3.11.7, Node 20 LTS
- 32 GB RAM
- PostgreSQL 15.5 (managed service)
- Redis 7.2 (managed service)
- CDN for frontend
- Load balancer

---

# Summary Checklist

Before starting development, ensure:

- [ ] Python 3.11+ installed
- [ ] Node.js 20+ installed
- [ ] PostgreSQL 15+ installed and running
- [ ] Redis installed (optional but recommended)
- [ ] Git installed
- [ ] Code editor setup (VS Code recommended)
- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Frontend dependencies installed (`npm install`)
- [ ] Database created (`createdb pmi_db`)
- [ ] Environment variables configured (`.env` files)
- [ ] Datasets generated (`python scripts/generate_datasets.py`)
- [ ] Models trained (`python scripts/train_models.py`)
- [ ] Backend running (`http://localhost:8000`)
- [ ] Frontend running (`http://localhost:5173`)

---

**If all items checked → You're ready to build! 🚀**

For additional help, see:
- [README.md](README.md) - Quick start guide
- [DESIGN.md](DESIGN.md) - Architecture overview
- [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) - Detailed troubleshooting

---

**Last Updated:** February 2026  
**Maintained By:** PMI Team
