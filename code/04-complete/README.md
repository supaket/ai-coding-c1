# Order Service API

A production-ready FastAPI microservice for order management with complete CRUD operations for Users, Products, Orders, Inventory, and Notifications.

## 🏗️ Architecture

```
app/
├── api/v1/           # REST API endpoints
│   ├── health.py     # Health check endpoint
│   ├── users.py      # User management
│   ├── products.py   # Product catalog
│   ├── orders.py     # Order operations
│   ├── inventory.py  # Stock management
│   └── notifications.py  # Notification system
├── models/           # SQLAlchemy ORM models
├── schemas/          # Pydantic validation schemas
├── repositories/     # Data access layer
├── services/         # Business logic layer
└── core/             # Database & configuration
```

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- OR Python 3.11+ (for local development)

### Option 1: Docker (Recommended)

```bash
# Build and run with docker-compose
./docker-compose-up.sh

# Or build and run manually
./docker-build.sh
./docker-run.sh
```

### Option 2: Local Development

```bash
# Setup Python environment
./setup.sh

# Run the application
./run.sh
```

## 🐳 Docker Commands

| Script | Description |
|--------|-------------|
| `./docker-build.sh` | Build Docker image |
| `./docker-run.sh [port]` | Run standalone container (default: 8000) |
| `./docker-compose-up.sh` | Start with docker-compose |
| `./docker-compose-up.sh down` | Stop all services |
| `./docker-compose-up.sh logs` | View logs |
| `./docker-compose-up.sh status` | Show service status |
| `./docker-stop.sh` | Stop all containers |
| `./docker-clean.sh` | Remove containers and images |
| `./docker-clean.sh --all` | Remove everything including data |

## 📍 API Endpoints

Once running, access the API at:

| Endpoint | Description |
|----------|-------------|
| http://localhost:8000/docs | Swagger UI (Interactive API docs) |
| http://localhost:8000/redoc | ReDoc (Alternative API docs) |
| http://localhost:8000/api/v1/health | Health check |

### API Routes

| Method | Endpoint | Description |
|--------|----------|-------------|
| **Users** |||
| GET | `/api/v1/users` | List all users |
| POST | `/api/v1/users` | Create user |
| GET | `/api/v1/users/{id}` | Get user by ID |
| PUT | `/api/v1/users/{id}` | Update user |
| DELETE | `/api/v1/users/{id}` | Delete user |
| **Products** |||
| GET | `/api/v1/products` | List all products |
| POST | `/api/v1/products` | Create product |
| GET | `/api/v1/products/{id}` | Get product by ID |
| PUT | `/api/v1/products/{id}` | Update product |
| DELETE | `/api/v1/products/{id}` | Delete product |
| **Orders** |||
| GET | `/api/v1/orders` | List all orders |
| POST | `/api/v1/orders` | Create order |
| GET | `/api/v1/orders/{id}` | Get order by ID |
| PUT | `/api/v1/orders/{id}/status` | Update order status |
| DELETE | `/api/v1/orders/{id}` | Cancel order |
| **Inventory** |||
| GET | `/api/v1/inventory/{product_id}` | Get stock level |
| PUT | `/api/v1/inventory/{product_id}` | Update stock |
| POST | `/api/v1/inventory/{product_id}/reserve` | Reserve stock |
| POST | `/api/v1/inventory/{product_id}/release` | Release stock |
| **Notifications** |||
| GET | `/api/v1/notifications` | List notifications |
| POST | `/api/v1/notifications` | Create notification |
| PUT | `/api/v1/notifications/{id}/read` | Mark as read |

## 🧪 Testing

```bash
# Run all tests
./run.sh test

# Or directly with pytest
source venv/bin/activate
pytest tests/ -v
```

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ENVIRONMENT` | `development` | Runtime environment |
| `DATABASE_URL` | `sqlite+aiosqlite:///./orders.db` | Database connection |

### Docker Compose Environment

Edit `docker-compose.yml` to customize:

```yaml
environment:
  - ENVIRONMENT=development
  - DATABASE_URL=sqlite+aiosqlite:///./data/orders.db
```

## 📁 Project Structure

```
04-complete/
├── app/                    # Application source code
├── tests/                  # Test suite
├── data/                   # SQLite database (created at runtime)
├── venv/                   # Python virtual environment
├── Dockerfile              # Multi-stage production build
├── docker-compose.yml      # Local development setup
├── docker-build.sh         # Build Docker image
├── docker-run.sh           # Run standalone container
├── docker-compose-up.sh    # Docker Compose management
├── docker-stop.sh          # Stop all containers
├── docker-clean.sh         # Cleanup script
├── setup.sh                # Local environment setup
├── run.sh                  # Local run script
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## 🔒 Security Features

- **Non-root user**: Container runs as `appuser`
- **Multi-stage build**: Minimal production image
- **Health checks**: Built-in container health monitoring
- **Read-only mounts**: App code mounted as read-only in dev

## 📝 Development Tips

### View Container Logs

```bash
# Docker Compose
docker-compose logs -f

# Standalone container
docker logs -f order-service-api
```

### Access Container Shell

```bash
docker exec -it order-service-api /bin/bash
```

### Rebuild After Code Changes

```bash
# With docker-compose (auto-rebuilds)
./docker-compose-up.sh restart

# Standalone
./docker-build.sh && ./docker-run.sh
```

## 📜 License

MIT License - See LICENSE file for details.
