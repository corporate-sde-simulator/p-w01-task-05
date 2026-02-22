"""
Database Connection wrapper.

Represents a single database connection with lifecycle tracking.

Author: Meera Iyer
Last Modified: 2026-02-05
"""

import time
import uuid


class Connection:
    def __init__(self, host, port, database):
        self.id = str(uuid.uuid4())[:8]
        self.host = host
        self.port = port
        self.database = database
        self.created_at = time.time()
        self.last_used_at = time.time()
        self._is_open = True

    def execute(self, query, params=None):
        """Execute a SQL query on this connection."""
        if not self._is_open:
            raise ConnectionError(f"Connection {self.id} is closed")
        self.last_used_at = time.time()
        # Simulate query execution
        return {"status": "ok", "query": query, "params": params}

    def health_check(self):
        """Verify the connection is still alive and usable."""
        # BUG: Always returns True — should actually test the connection
        return True

    def close(self):
        """Close the connection."""
        self._is_open = False

    def is_open(self):
        return self._is_open

    def __repr__(self):
        status = "open" if self._is_open else "closed"
        return f"Connection(id={self.id}, db={self.database}, status={status})"
