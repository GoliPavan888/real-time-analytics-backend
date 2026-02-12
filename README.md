# Real-Time Analytics Backend

A robust backend API for a simulated real-time analytics service built using **FastAPI**, **Redis**, and **Docker**. The system demonstrates production-grade backend practices including caching, rate limiting, and circuit breaker patterns to ensure high availability and resilience.

This project simulates a backend powering a real-time analytics dashboard capable of handling load spikes and external service failures.

---

## Features

- RESTful API for metric ingestion and analytics retrieval
- Redis-backed read-through caching
- IP-based rate limiting using Redis
- Circuit breaker pattern for external service protection
- Docker containerization with docker-compose orchestration
- Health check endpoints
- Unit and integration tests
- Configurable environment variables
- Auto-generated API documentation

---

## Tech Stack

- FastAPI (Python)
- Redis
- Docker & Docker Compose
- Pytest
- Async Redis client

---

## Quick Start

### Prerequisites
Install:

- Docker
- Docker Compose

---

### Setup & Run

Clone repository:

```bash
git clone <your-repo-url>
cd real-time-analytics-backend
```

Create environment file (optional):

**Linux/macOS:**

```bash
cp .env.example .env
```

**Windows:**

```cmd
copy .env.example .env
```

Run services:

```bash
docker-compose up --build
```

Application becomes available at:

http://localhost:8000

Swagger API docs available at:

http://localhost:8000/docs

## API Endpoints

### Health Check

```bash
GET /health
```

Response:

```json
{
  "status": "healthy"
}
```

### Ingest Metric

```bash
POST /api/metrics
```

Request body:

```json
{
  "timestamp": "2026-02-08T10:00:00",
  "value": 50,
  "type": "cpu"
}
```

Response:

```json
{
  "message": "Metric received"
}
```

Returns:

- 201 Created on success
- 429 Too Many Requests if rate limit exceeded

Rate-limited per client IP.

### Metrics Summary

```bash
GET /api/metrics/summary?type=cpu&period=daily
```

Example response:

```json
{
  "type": "cpu",
  "period": "daily",
  "average_value": 50,
  "count": 1,
  "external_data": {
    "external_source": "ok",
    "value": 170
  }
}
```

Results are cached in Redis for faster repeated responses.

## Configuration

Environment variables (see .env.example):

| Variable | Description | Default |
|----------|-------------|---------|
| REDIS_HOST | Redis hostname | redis |
| REDIS_PORT | Redis port | 6379 |
| APP_PORT | App port | 8000 |
| CACHE_TTL_SECONDS | Cache lifetime | 300 |
| RATE_LIMIT_THRESHOLD | Requests per window | 5 |
| RATE_LIMIT_WINDOW_SECONDS | Window size | 60 |
| CIRCUIT_BREAKER_FAILURE_THRESHOLD | Failures before open | 3 |
| CIRCUIT_BREAKER_RESET_TIMEOUT | Reset timeout | 10 |
| EXTERNAL_SERVICE_FAILURE_RATE | Simulated failure rate | 0.1 |

## Running Tests

Run all tests:

```bash
docker-compose run --rm test-runner pytest -v
```

Run individual tests:

```bash
docker-compose run --rm test-runner pytest tests/test_rate_limiter.py -v
```

## Architecture Overview

```
src/
 ├── main.py
 ├── api/
 │    └── metrics.py
 ├── services/
 │    ├── cache_service.py
 │    ├── rate_limit_service.py
 │    ├── circuit_breaker_service.py
 │    └── external_data_simulator.py
 └── config/
      └── settings.py
tests/
Dockerfile
docker-compose.yml
```

## Resilience Patterns Implemented

### Redis Caching
Summary responses are cached using Redis with TTL to reduce computation and improve performance.

Rate Limiting
Requests are tracked per IP using Redis sorted sets to prevent abuse.

Circuit Breaker
External service failures are monitored. When failures exceed threshold:

Circuit opens

Calls immediately fallback

Later transitions to half-open for recovery testing
