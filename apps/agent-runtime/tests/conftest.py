import sys
from unittest.mock import MagicMock

# Mock langgraph.checkpoint.postgres since it might be missing in the test env
mock_postgres = MagicMock()
sys.modules["langgraph.checkpoint.postgres"] = mock_postgres

# Also mock psycopg_pool
mock_pool = MagicMock()
sys.modules["psycopg_pool"] = mock_pool
