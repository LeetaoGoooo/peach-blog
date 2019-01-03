import pytest
from . import app

client = app.test_client()

def test_dashboard():
    res = client.get("/api/v1/dashboard")
    assert b'sum_device_visit' in res.data