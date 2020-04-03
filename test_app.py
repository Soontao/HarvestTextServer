import pytest
from app import app


@pytest.fixture
def client():
    """
    create test client for pytest
    """
    app.config['TESTING'] = True

    with app.test_client() as c:
        with app.app_context():
            yield c


def test_metric_api(client):
    """Test Metric API Works."""

    res = client.get('/').get_json()
    assert res["code"] == 200
    assert "service" in res
    assert "docs" in res
