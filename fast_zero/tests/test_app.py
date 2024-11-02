from fastapi.testclient import TestClient

from fast_zero.app import app

cliente = TestClient(app)
