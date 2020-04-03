import os
import tempfile

import pytest
from flask import json
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True

    with app.test_client() as client:
        with app.app_context():
            yield client


def test_metric_api(client):
    """Test Metric API Works."""

    rv = client.get('/').get_json()
    assert rv["code"] == 200
    assert "service" in rv
    assert "docs" in rv
