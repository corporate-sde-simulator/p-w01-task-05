"""
Tests for Connection Pool Manager.
"""

import pytest
import time
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from connection import Connection
from connectionPool import ConnectionPool


class TestConnection:
    def test_create_connection(self):
        conn = Connection('localhost', 5432, 'test_db')
        assert conn.is_open()
        assert conn.database == 'test_db'

    def test_execute_query(self):
        conn = Connection('localhost', 5432, 'test_db')
        result = conn.execute("SELECT 1")
        assert result['status'] == 'ok'

    def test_execute_on_closed_connection(self):
        conn = Connection('localhost', 5432, 'test_db')
        conn.close()
        with pytest.raises(ConnectionError):
            conn.execute("SELECT 1")

    def test_health_check(self):
        conn = Connection('localhost', 5432, 'test_db')
        assert conn.health_check() is True

    def test_last_used_updates_on_execute(self):
        conn = Connection('localhost', 5432, 'test_db')
        before = conn.last_used_at
        time.sleep(0.01)
        conn.execute("SELECT 1")
        assert conn.last_used_at > before


class TestConnectionPool:
    def test_pool_initializes_with_min_connections(self):
        pool = ConnectionPool(min_size=3, max_size=10)
        stats = pool.get_stats()
        assert stats['available'] == 3

    def test_acquire_returns_connection(self):
        pool = ConnectionPool(min_size=2, max_size=5)
        conn = pool.acquire()
        assert conn is not None
        assert conn.is_open()

    def test_acquire_tracks_in_use(self):
        pool = ConnectionPool(min_size=2, max_size=5)
        conn = pool.acquire()
        stats = pool.get_stats()
        assert stats['in_use'] == 1
        assert stats['available'] == 1

    def test_release_returns_connection_to_pool(self):
        pool = ConnectionPool(min_size=2, max_size=5)
        conn = pool.acquire()
        pool.release(conn)
        stats = pool.get_stats()
        assert stats['available'] >= 2

    def test_pool_respects_max_size(self):
        pool = ConnectionPool(min_size=1, max_size=2, acquire_timeout=1)
        c1 = pool.acquire()
        c2 = pool.acquire()
        with pytest.raises(TimeoutError):
            pool.acquire()

    def test_stale_connection_replaced(self):
        pool = ConnectionPool(min_size=1, max_size=5, max_idle_seconds=0)
        conn = pool.acquire()
        time.sleep(0.01)
        pool.release(conn)
        stats = pool.get_stats()
        assert stats['available'] >= 1  # Replaced with fresh connection

    def test_close_all(self):
        pool = ConnectionPool(min_size=3, max_size=5)
        pool.close_all()
        stats = pool.get_stats()
        assert stats['available'] == 0
        assert stats['in_use'] == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
