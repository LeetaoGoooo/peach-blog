import pytest
from app import create_app

app = create_app('testing')
client = app.test_client()

def test_dashboard():
    res = client.get("/api/v1/dashboard")
    assert b'sum_device_visit' in res.data