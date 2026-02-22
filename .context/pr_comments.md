# PR #365 Review — Connection Pool Manager (by Meera Iyer)

## Reviewer: Amit Desai (Database Lead) — Feb 5, 2026

---

**Overall:** Good foundation but needs fixes before merge.

### `connectionPool.py`

> **Line 41** — `acquire` method:  
> You pop from `_available` but never add to `_in_use`. This means the pool doesn't know which connections are checked out.

> **Line 55** — `release` method:  
> You add back to `_available` but never remove from `_in_use`. Over time, `_in_use` grows forever, and `_available` can have duplicates.

> **Line 73** — `_is_stale` method:  
> You're comparing `time.time() - conn.created_at`, but it should be `time.time() - conn.last_used_at`. A connection that was created a long time ago but recently used is not stale.

### `connection.py`

> The `Connection` class looks fine. Good use of `last_used_at` tracking.  
> One note: `health_check()` just returns `True` — it should actually ping the database.

---

**Meera Iyer** — Feb 6, 2026

> Good catches Amit. The acquire/release tracking is definitely broken. I'll try to fix it before going on call, but if not, the intern can take it.
