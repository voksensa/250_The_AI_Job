import pytest
from fastapi.testclient import TestClient
from sandbox_proxy.main import app
from sandbox_proxy.settings import settings
from pathlib import Path

client = TestClient(app)

@pytest.fixture
def mock_workspace(tmp_path):
    # Mock the workspace root to a temp directory
    original_root = settings.WORKSPACE_ROOT
    settings.WORKSPACE_ROOT = tmp_path
    
    # Create a dummy task and file
    task_dir = tmp_path / "task-123"
    task_dir.mkdir()
    (task_dir / "index.html").write_text("<h1>Hello World</h1>")
    
    yield tmp_path
    
    settings.WORKSPACE_ROOT = original_root

def test_health_check():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_serve_file_success(mock_workspace):
    # Test accessing index.html via subdomain
    headers = {"Host": "task-123.localhost:3001"}
    response = client.get("/", headers=headers)
    assert response.status_code == 200
    assert "<h1>Hello World</h1>" in response.text

def test_serve_file_explicit_path(mock_workspace):
    headers = {"Host": "task-123.localhost:3001"}
    response = client.get("/index.html", headers=headers)
    assert response.status_code == 200
    assert "<h1>Hello World</h1>" in response.text

def test_default_host_shows_welcome():
    # TestClient sends 'testserver' by default
    response = client.get("/")
    assert response.status_code == 200
    assert "Sandbox Proxy Running" in response.json()["message"]

def test_invalid_domain_root():
    headers = {"Host": "example.com"}
    response = client.get("/", headers=headers)
    assert response.status_code == 200
    assert "Sandbox Proxy Running" in response.json()["message"]

def test_invalid_domain_with_path():
    headers = {"Host": "example.com"}
    response = client.get("/somefile.html", headers=headers)
    assert response.status_code == 404
    assert "Domain not recognized" in response.json()["detail"]

def test_task_not_found(mock_workspace):
    headers = {"Host": "task-999.localhost:3001"}
    response = client.get("/", headers=headers)
    assert response.status_code == 404

def test_path_traversal_attempt(mock_workspace):
    headers = {"Host": "../task-123.localhost:3001"}
    response = client.get("/", headers=headers)
    assert response.status_code == 400
    
def test_direct_access_root():
    # Accessing localhost:3001 directly
    headers = {"Host": "localhost:3001"}
    response = client.get("/", headers=headers)
    assert response.status_code == 200
    assert "Sandbox Proxy Running" in response.json()["message"]
