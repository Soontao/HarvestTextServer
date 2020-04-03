import pytest
from flask.testing import FlaskClient
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


def test_language_detection(client: FlaskClient):
    """Test Language Detection API"""

    res = client.get(f"/api/v1/nlp/lang_detect?text=hello world!").get_json()
    assert res["code"] == 200
    assert res["lang"] == "en"

    res = client.get(f"/api/v1/nlp/lang_detect?text=你好世界·!").get_json()
    assert res["code"] == 200
    assert res["lang"] == "zh"

    # error test
    res = client.get(f"/api/v1/nlp/lang_detect").get_json()
    assert res["code"] == 400
    assert res["error_type"] == "ParameterLostError"
    assert "error" in res
