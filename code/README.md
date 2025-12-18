# 🧪 AI Coding Workshop - Code Artifacts

Ready-to-use code for each lab stage. **Jump to any point instantly!**

## 📁 Lab Structure

```
code/
├── 01-legacy-app/     ← Start here: Flask monolith to analyze
├── 02-scaffold/       ← Lab 2 result: FastAPI + models + schemas
├── 03-business-logic/ ← Lab 3 result: + repository + service + routes
└── 04-complete/       ← Lab 4 result: + tests + Docker (final solution)
```

---

## 🚀 Quick Start Commands

### Lab 1: Analyze Legacy App
```bash
cd 01-legacy-app
pip install -r requirements.txt
python seed_data.py
python app.py
# Open: http://localhost:5000/api/orders
```

### Lab 2: Start Microservice Scaffold
```bash
cd 02-scaffold
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
# Open: http://localhost:8000/docs
```

### Lab 3: Working Business Logic
```bash
cd 03-business-logic
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
# Try: POST http://localhost:8000/api/v1/orders
```

### Lab 4: Complete Solution + Tests
```bash
cd 04-complete
pip install -r requirements.txt

# Run app
uvicorn app.main:app --reload --port 8000

# Run tests
pytest tests/ -v

# Docker
docker build -t order-service .
docker-compose up
```

---

## 📝 Lab Progression

| Lab | Focus | Files Added | Duration |
|-----|-------|-------------|----------|
| 1 | Analyze Legacy | Analysis notes | 20 min |
| 2 | Scaffold | models/, schemas/, health.py | 25 min |
| 3 | Business Logic | repositories/, services/, orders.py | 25 min |
| 4 | Testing | tests/, Dockerfile | 20 min |

---

## 🔑 Key Files by Lab

### Lab 2 - Scaffold
- `app/core/database.py` - Async SQLAlchemy setup
- `app/models/order.py` - Order model (SQLAlchemy 2.0)
- `app/models/order_item.py` - OrderItem model
- `app/schemas/order.py` - Pydantic schemas

### Lab 3 - Business Logic
- `app/repositories/order_repository.py` - Data access
- `app/services/order_service.py` - Business rules
- `app/api/v1/orders.py` - REST endpoints
- `app/core/exceptions.py` - Custom exceptions

### Lab 4 - Testing
- `tests/conftest.py` - Pytest fixtures
- `tests/test_order_service.py` - Unit tests
- `tests/test_api_orders.py` - Integration tests
- `Dockerfile` - Production container
- `docker-compose.yml` - Local development

---

## 👨‍🏫 Instructor Tips

1. **Demo Flow**: Legacy (5000) → Scaffold (8000) → Complete (8000)
2. **Show side-by-side**: Legacy route vs. Clean architecture
3. **Run tests live**: `pytest -v --tb=short`
4. **Highlight AI prompts** from workshop slides

## 🎓 Student Tips

1. **Stuck?** Check the next lab folder for the solution
2. **Compare**: Use `diff` to see what changed between labs
3. **Test often**: Run `pytest` after each change
4. **AI prompts**: Use the prompts from slides, not just copy-paste
