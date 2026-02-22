# PLATFORM-2838: Implement database connection pool manager

**Status:** In Progress Â· **Priority:** High
**Sprint:** Sprint 23 Â· **Story Points:** 5
**Reporter:** Amit Desai (Database Team Lead) Â· **Assignee:** You (Intern)
**Created:** Â· **Due:** End of sprint (Friday)
**Labels:** `backend`, `database`, `python`, `infrastructure`
**Epic:** PLATFORM-2820 (Database Reliability v2)
**Task Type:** Bug Fix

---

## Description

Our services are opening a new database connection for every request, causing connection exhaustion under load (max 100 connections on the PostgreSQL instance). We need a connection pool that reuses connections and manages their lifecycle.

Meera (senior dev) wrote the initial pool but was pulled into an incident. Her implementation has bugs in the connection checkout/checkin logic and doesn't properly handle stale connections.

## Requirements

- Pool should maintain a configurable min/max number of connections
- Connections should be reused (checkout/checkin pattern)
- Stale connections (idle > 5 minutes) should be automatically closed
- Pool should block (with timeout) when all connections are in use
- Health check: validate connections before returning to callers

## Acceptance Criteria

- [ ] Pool initializes with `min_size` connections
- [ ] `acquire()` returns an available connection or waits
- [ ] `release()` returns connection to the pool
- [ ] Stale connections are detected and replaced
- [ ] Pool respects `max_size` limit
- [ ] Timeout works when pool is exhausted
- [ ] All unit tests pass

## Design Notes

See `docs/DESIGN.md` for pooling strategy decisions.
See `.context/pr_comments.md` for Meera's PR feedback.
