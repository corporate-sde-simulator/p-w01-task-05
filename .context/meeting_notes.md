# Meeting Notes — Sprint 23 Standup

**Date:** Feb 11, 2026  
**Attendees:** Amit (DB Lead), Meera, Sanjay, Intern

---

## Connection Pool Work

- **Amit:** We hit 98 out of 100 PostgreSQL connections during the morning spike. This is critical — we need pooling before we start dropping requests. @Intern, I'm assigning PLATFORM-2838 to you. Meera's code is in the repo.

- **Meera:** The basic pool structure works. There's a bug in how I'm tracking checked-out connections — I think I'm not removing them from the available set, so the same connection gets handed to two threads. Also the staleness check uses the wrong timestamp.

- **Sanjay:** Make sure the health check actually runs a query. A TCP connection can be alive but the database session can be dead.

## Action Items

- [ ] @Intern — Fix connection pool bugs (PLATFORM-2838)
- [ ] @Meera — Available for questions via Slack
- [ ] @Sanjay — Test with load generator once pool is fixed
