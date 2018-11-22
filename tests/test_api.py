import pytest
from app import create_app

app = create_app('testing')
client = app.test_client()


def test_get_today_visit_chart():
    return client.get("/api/v1/dashboard")