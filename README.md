# Real-Time Analytics Backend

A robust backend API for a simulated real-time analytics service, built with FastAPI, Redis, and Docker. Implements advanced caching, rate limiting, and circuit breaker patterns for high availability and fault tolerance.

## Features

- **RESTful API**: POST /api/metrics for ingesting metrics, GET /api/metrics/summary for aggregated data
- **Redis Caching**: Read-through caching for summary endpoints with configurable TTL
- **Rate Limiting**: IP-based rate limiting on metric ingestion using Redis
- **Circuit Breaker**: Protects external service calls with configurable failure thresholds
- **Docker Containerization**: Fully containerized with docker-compose for easy deployment
- **Health Checks**: Built-in health endpoints for monitoring
- **Comprehensive Tests**: Unit and integration tests covering all core functionality

## Quick Start

### Prerequisites
- Docker and Docker Compose installed

### Setup
1. Clone the repository
2. Navigate to the project directory
3. Copy environment variables: `cp .env.example .env` (optional, defaults are set)
4. Run with Docker Compose: `docker-compose up --build`

The API will be available at http://localhost:8000

## API Documentation

### POST /api/metrics
Ingest a new metric.

**Request Body:**
```json
{
  "timestamp": "2023-01-01T00:00:00Z",
  "value": 75.5,
  "type": "cpu_usage"
}
```

**Response:** 201 Created
```json
{
  "message": "Metric received"
}
```

Rate limited to 5 requests per minute per IP. Exceeding returns 429 with Retry-After header.

### GET /api/metrics/summary
Retrieve aggregated metrics summary.

**Query Parameters:**
- `type`: Metric type (e.g., cpu_usage)
- `period`: Aggregation period (e.g., daily)

**Response:** 200 OK
```json
{
  "type": "cpu_usage",
  "period": "daily",
  "average_value": 75.3,
  "count": 100,
  "external_data": {
    "external_source": "ok",
    "value": 150
  }
}
```

Cached for 5 minutes by default.

### GET /health
Health check endpoint.

**Response:** 200 OK
```json
{
  "status": "healthy"
}
```

## Configuration

Environment variables (see .env.example):

- `REDIS_HOST`: Redis host (default: redis)
- `REDIS_PORT`: Redis port (default: 6379)
- `APP_PORT`: Application port (default: 8000)
- `CACHE_TTL_SECONDS`: Cache TTL in seconds (default: 300)
- `RATE_LIMIT_THRESHOLD`: Requests per window (default: 5)
- `RATE_LIMIT_WINDOW_SECONDS`: Rate limit window in seconds (default: 60)
- `CIRCUIT_BREAKER_FAILURE_THRESHOLD`: Failures before opening circuit (default: 3)
- `CIRCUIT_BREAKER_RESET_TIMEOUT`: Seconds to wait before half-open (default: 10)
- `EXTERNAL_SERVICE_FAILURE_RATE`: Simulated failure rate (default: 0.1)

## Running Tests

### Unit Tests
```bash
docker-compose exec app pytest tests/test_rate_limiter.py -v
```

### Integration Tests
```bash
docker-compose exec app pytest tests/test_integration.py -v
```

### All Tests
```bash
docker-compose exec app pytest tests/ -v
```

## Architecture

- **src/main.py**: FastAPI application entry point
- **src/api/metrics.py**: API endpoints
- **src/services/**: Business logic services (cache, rate limiter, circuit breaker, external simulator)
- **src/config/settings.py**: Configuration management
- **tests/**: Unit and integration tests
- **Dockerfile**: Application containerization
- **docker-compose.yml**: Multi-container orchestration

## Resilience Patterns

### Caching
Read-through caching using Redis. Summary computations are cached with TTL to reduce load.

### Rate Limiting
Sliding window counter using Redis sorted sets. Limits requests per IP to prevent abuse.

### Circuit Breaker
Three-state pattern (Closed/Open/Half-Open) to handle external service failures gracefully.

## Development

To run locally without Docker:
1. Install dependencies: `pip install -r requirements.txt`
2. Start Redis: `redis-server`
3. Run app: `uvicorn src.main:app --reload`

## License

MIT License
