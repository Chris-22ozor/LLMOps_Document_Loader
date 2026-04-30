# tests/test_unit_cases.py

import pytest
from fastapi.testclient import TestClient
from api.main import app   # or your FastAPI entrypoint

client = TestClient(app)

def test_home():
    response = client.get("/") # client.get (hme url)  this gives the response (html page)
    assert response.status_code == 200 #here we are checking if the html is being called succesfuly
    assert "Document Portal" in response.text # here we are if the title document portal is in response.text in the html file