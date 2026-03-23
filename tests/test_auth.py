import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models.user import User
from app.auth import hash_password

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_auth.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def register_user(email="test@example.com", username="testuser", password="Test1234"):
    return client.post("/api/auth/register", json={
        "email": email, "username": username, "password": password
    })


def login_user(email="test@example.com", password="Test1234"):
    return client.post("/api/auth/login", json={"email": email, "password": password})


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200


def test_register():
    resp = register_user()
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert data["role"] == "user"


def test_register_duplicate_email():
    register_user()
    resp = register_user(username="other")
    assert resp.status_code == 400


def test_register_duplicate_username():
    register_user()
    resp = register_user(email="other@example.com")
    assert resp.status_code == 400


def test_login():
    register_user()
    resp = login_user()
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_login_wrong_password():
    register_user()
    resp = login_user(password="wrong")
    assert resp.status_code == 401


def test_get_me():
    register_user()
    tokens = login_user().json()
    resp = client.get("/api/auth/me", headers={"Authorization": f"Bearer {tokens['access_token']}"})
    assert resp.status_code == 200
    assert resp.json()["email"] == "test@example.com"


def test_get_me_no_token():
    resp = client.get("/api/auth/me")
    assert resp.status_code == 401


def test_change_password():
    register_user()
    tokens = login_user().json()
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    resp = client.put("/api/auth/change-password", json={
        "current_password": "Test1234", "new_password": "NewPass5678"
    }, headers=headers)
    assert resp.status_code == 200

    # Yeni şifreyle giriş yap
    resp = login_user(password="NewPass5678")
    assert resp.status_code == 200


def test_refresh_token():
    register_user()
    tokens = login_user().json()
    resp = client.post("/api/auth/refresh", json={"refresh_token": tokens["refresh_token"]})
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_admin_required():
    register_user()
    tokens = login_user().json()
    resp = client.get("/api/admin/users", headers={"Authorization": f"Bearer {tokens['access_token']}"})
    assert resp.status_code == 403
