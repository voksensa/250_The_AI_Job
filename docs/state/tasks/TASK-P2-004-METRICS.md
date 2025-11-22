# TASK-P2-004-METRICS: Add Basic Metrics Endpoint

**Priority**: MEDIUM  
**Order**: Task 4 of 4 (Phase 2 Foundation)  
**Depends On**: TASK-P2-003-LOGGING  
**Estimated**: 2 hours

---

## Objective

Expose basic metrics (requests, errors, latency) for production monitoring.

**Golden Rule**: Rule 4.11 from RB-003 (Tier 2)

---

## Current State

**No metrics exposed**:
- Can't track request volume
- Can't measure latency
- Can't monitor error rates
- No health dashboards

---

## Tasks

### Phase A: Install Prometheus Client (15min)

**Install**: `prometheus-client`

**Add to**: `apps/agent-runtime/requirements.txt`

---

### Phase B: Create Metrics Helpers (45min)

**Create**: `apps/agent-runtime/src/agent_runtime/utils/metrics.py`

```python
from prometheus_client import Counter, Histogram, Gauge

# Request metrics
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

# Task metrics
tasks_created_total = Counter('tasks_created_total', 'Total tasks created')
tasks_completed_total = Counter('tasks_completed_total', 'Total tasks completed')
tasks_failed_total = Counter('tasks_failed_total', 'Total tasks failed')

# LangGraph metrics
graph_node_executions = Counter(
    'graph_node_executions',
    'Graph node executions',
    ['node_name', 'status']
)
```

---

### Phase C: Add Middleware (30min)

**Update**: `apps/agent-runtime/src/agent_runtime/main.py`

```python
from prometheus_client import make_asgi_app

# Add metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Add request tracking middleware
@app.middleware("http")
async def track_requests(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    
    http_requests_total.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    http_request_duration_seconds.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)
    
    return response
```

---

### Phase D: Instrument Key Paths (30min)

**Update**:
- `api/routers/tasks.py`: Track task creation, completion, failures
- `graph/nodes/`: Track node executions

```python
# Example
tasks_created_total.inc()
graph_node_executions.labels(node_name="planner", status="success").inc()
```

---

## Success Criteria

✅ **Endpoint**: `/metrics` returns Prometheus format  
✅ **HTTP Metrics**: Requests, latency tracked  
✅ **Task Metrics**: Create, complete, fail counted  
✅ **Graph Metrics**: Node executions tracked  
✅ **Documentation**: Metrics documented in README

---

## After Completion

**Phase 2 Foundation Complete**:
- ✅ Constitution cleaned
- ✅ OpenAPI spec created
- ✅ Logging structured
- ✅ Metrics exposed

**Next**: Start main Phase 2 work (Synthetic User QA)
