# ADR-011: Connection Pooling Strategy

**Date:**  
**Status:** Accepted  
**Authors:** Amit Desai, Meera Iyer

## Decision

Implement a **custom connection pool** with checkout/checkin semantics rather than relying on ORM-level pooling.

## Context

PostgreSQL instance has a 100-connection limit. Services currently open new connections per request (~200 req/s at peak). We need to share connections across request handlers.

## Options Considered

| Option | Pros | Cons |
|---|---|---|
| No pooling (current) | Simple | Connection exhaustion |
| ORM pooling (SQLAlchemy) | Built-in | Tight coupling to ORM |
| Custom pool | Full control, framework-agnostic | More code to maintain |
| PgBouncer (external) | Zero code change | Ops overhead, another service |

## Rationale

- Custom pool gives us full control over health checks and staleness detection
- Framework-agnostic â€” works with any database driver
- Can add metrics/logging specific to our monitoring

## Consequences

- Must handle thread safety manually
- Must implement health checks and stale connection eviction
- Connection lifecycle is our responsibility (not the ORM's)
