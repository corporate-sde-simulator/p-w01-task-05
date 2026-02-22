"""
Connection Pool Manager.

Manages a pool of database connections with checkout/checkin pattern.

Author: Meera Iyer 
Last Modified: 2026-02-05
"""

import time
import threading
from connection import Connection


class ConnectionPool:
    def __init__(self, host='localhost', port=5432, database='app_db',
                 min_size=5, max_size=20, max_idle_seconds=300,
                 acquire_timeout=30):
        self.host = host
        self.port = port
        self.database = database
        self.min_size = min_size
        self.max_size = max_size
        self.max_idle_seconds = max_idle_seconds
        self.acquire_timeout = acquire_timeout

        self._available = []
        self._in_use = set()
        self._lock = threading.Lock()

        # Initialize pool with minimum connections
        for _ in range(min_size):
            conn = self._create_connection()
            self._available.append(conn)

    def _create_connection(self):
        """Create a new database connection."""
        return Connection(self.host, self.port, self.database)

    def acquire(self):
        """Acquire a connection from the pool. Blocks if none available."""
        start_time = time.time()

        while True:
            with self._lock:
                # Try to get an available connection
                if self._available:
                    conn = self._available.pop()
                    # BUG: Never adds conn to _in_use tracking set
                    if conn.is_open() and conn.health_check():
                        conn.last_used_at = time.time()
                        return conn
                    else:
                        # Connection is dead, discard it
                        continue

                # No available connections — can we create a new one?
                total = len(self._available) + len(self._in_use)
                if total < self.max_size:
                    conn = self._create_connection()
                    # BUG: doesn't add to _in_use
                    return conn

            # Pool exhausted — wait and retry
            elapsed = time.time() - start_time
            if elapsed >= self.acquire_timeout:
                raise TimeoutError(
                    f"Could not acquire connection within {self.acquire_timeout}s"
                )
            time.sleep(0.1)

    def release(self, conn):
        """Return a connection to the pool."""
        with self._lock:
            # BUG: Never removes conn from _in_use
            if self._is_stale(conn):
                conn.close()
                # Replace with fresh connection if below min_size
                if len(self._available) < self.min_size:
                    self._available.append(self._create_connection())
            else:
                conn.last_used_at = time.time()
                self._available.append(conn)

    def _is_stale(self, conn):
        """Check if a connection has been idle too long."""
        # BUG: Uses created_at instead of last_used_at
        return (time.time() - conn.created_at) > self.max_idle_seconds

    def close_all(self):
        """Close all connections in the pool."""
        with self._lock:
            for conn in self._available:
                conn.close()
            self._available.clear()
            self._in_use.clear()

    def get_stats(self):
        """Return pool statistics."""
        with self._lock:
            return {
                'available': len(self._available),
                'in_use': len(self._in_use),
                'total': len(self._available) + len(self._in_use),
                'max_size': self.max_size
            }
