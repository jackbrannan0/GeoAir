"""API endpoint tests"""

def test_health_check(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data


def test_status_endpoint(client):
    """Test status endpoint"""
    response = client.get("/status")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "running"
    assert "version" in data
