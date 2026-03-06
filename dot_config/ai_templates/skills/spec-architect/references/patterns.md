# Architecture Patterns Reference

Quick reference for common architecture patterns. Load when designing specific system types.

## API Patterns

### REST Resource Naming
```
GET    /users           # List
POST   /users           # Create
GET    /users/:id       # Read
PATCH  /users/:id       # Update
DELETE /users/:id       # Delete
GET    /users/:id/orders  # Nested resource
POST   /users/:id/orders  # Create nested
```

### Pagination
```json
// Cursor-based (preferred)
{
  "data": [...],
  "next_cursor": "eyJpZCI6MTIzfQ==",
  "has_more": true
}

// Offset-based (simple but problematic at scale)
{
  "data": [...],
  "total": 1234,
  "page": 2,
  "per_page": 20
}
```

### Error Response Format
```json
{
  "error": {
    "code": "validation_error",
    "message": "Invalid request parameters",
    "details": [
      {"field": "email", "message": "Invalid format"}
    ]
  }
}
```

## Database Patterns

### Soft Deletes
```sql
ALTER TABLE users ADD COLUMN deleted_at TIMESTAMPTZ;
CREATE INDEX idx_users_active ON users(id) WHERE deleted_at IS NULL;
```

### Audit Trail
```sql
CREATE TABLE audit_log (
  id UUID PRIMARY KEY,
  table_name VARCHAR(100),
  record_id UUID,
  action VARCHAR(20), -- INSERT, UPDATE, DELETE
  old_data JSONB,
  new_data JSONB,
  actor_id UUID,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Optimistic Locking
```sql
UPDATE orders
SET status = 'shipped', version = version + 1
WHERE id = $1 AND version = $2;
-- Check rows affected; if 0, concurrent modification occurred
```

## Authentication Patterns

### JWT Structure
```json
{
  "header": {"alg": "RS256", "typ": "JWT"},
  "payload": {
    "sub": "user_123",
    "iat": 1704067200,
    "exp": 1704153600,
    "scope": ["read", "write"]
  }
}
```

### Token Lifecycle
- Access token: 15 min
- Refresh token: 7 days (rotate on use)
- Store refresh in httpOnly cookie
- Access token in memory only

## Caching Patterns

### Cache-Aside
```
1. Check cache
2. If miss → fetch from DB → write to cache
3. Return data
```

### Write-Through
```
1. Write to cache
2. Cache writes to DB
3. Return success
```

### Cache Invalidation
```
# Pattern: delete on write
user_update → DELETE cache:user:123

# Pattern: TTL-based
SET cache:user:123 {data} EX 300
```

## Queue Patterns

### Job Structure
```json
{
  "id": "job_abc123",
  "type": "email.send",
  "payload": {
    "to": "user@example.com",
    "template": "welcome"
  },
  "attempts": 0,
  "max_attempts": 3,
  "created_at": "2024-01-15T10:00:00Z"
}
```

### Retry Strategy
```
Attempt 1: immediate
Attempt 2: 1 min delay
Attempt 3: 5 min delay
Attempt 4: 30 min delay
Then → dead letter queue
```

## Event Patterns

### Event Structure
```json
{
  "id": "evt_xyz789",
  "type": "user.created",
  "timestamp": "2024-01-15T10:00:00Z",
  "data": {
    "user_id": "user_123",
    "email": "user@example.com"
  },
  "metadata": {
    "correlation_id": "req_abc",
    "source": "api"
  }
}
```

### Event Naming
```
# Format: <entity>.<action>
user.created
user.updated
user.deleted
order.placed
order.shipped
payment.succeeded
payment.failed
```

## File Upload Patterns

### Pre-signed URL Flow
```
1. Client → Server: "I want to upload file.pdf"
2. Server → Storage: Generate pre-signed URL
3. Server → Client: Return URL + fields
4. Client → Storage: Direct upload
5. Client → Server: "Upload complete, process it"
```

### Chunked Upload
```
1. Initiate: POST /uploads → upload_id
2. Parts: PUT /uploads/:id/parts/:num
3. Complete: POST /uploads/:id/complete
```

## Rate Limiting

### Token Bucket
```
Bucket size: 100 tokens
Refill rate: 10 tokens/second
Request cost: 1 token (or weighted)
```

### Sliding Window
```
Window: 1 minute
Limit: 100 requests
Key: user_id or IP
```

### Response Headers
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1704067260
```

## Observability

### Structured Logging
```json
{
  "timestamp": "2024-01-15T10:00:00.123Z",
  "level": "info",
  "message": "Order placed",
  "context": {
    "request_id": "req_abc",
    "user_id": "user_123",
    "order_id": "order_456",
    "duration_ms": 234
  }
}
```

### Key Metrics
```
# RED metrics (request-driven)
- Rate: requests/second
- Errors: error rate %
- Duration: latency percentiles

# USE metrics (resource-driven)
- Utilization: % capacity used
- Saturation: queue depth
- Errors: error count
```

### Trace Context
```
traceparent: 00-<trace-id>-<span-id>-01
tracestate: vendor=value
```
