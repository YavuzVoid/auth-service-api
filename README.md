# Auth Service API

JWT tabanlı kimlik doğrulama ve yetkilendirme servisi. Kayıt, giriş, token yenileme, şifre değiştirme ve role-based access control.

## Teknolojiler

- **FastAPI** - Web framework
- **SQLAlchemy** - ORM
- **JWT (python-jose)** - Token tabanlı kimlik doğrulama
- **Passlib + Bcrypt** - Şifre hashleme
- **PostgreSQL / SQLite** - Veritabanı
- **Pytest** - Test framework
- **Docker** - Containerization

## Kurulum

```bash
git clone https://github.com/YavuzVoid/auth-service-api.git
cd auth-service-api
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## API Endpoints

### Auth
| Method | Endpoint | Açıklama |
|--------|----------|----------|
| POST | `/api/auth/register` | Yeni kullanıcı kaydı |
| POST | `/api/auth/login` | Giriş yap, token al |
| POST | `/api/auth/refresh` | Token yenile |
| GET | `/api/auth/me` | Mevcut kullanıcı bilgisi |
| PUT | `/api/auth/change-password` | Şifre değiştir |

### Admin (admin rolü gerekli)
| Method | Endpoint | Açıklama |
|--------|----------|----------|
| GET | `/api/admin/users` | Tüm kullanıcıları listele |
| PATCH | `/api/admin/users/{id}/deactivate` | Kullanıcıyı devre dışı bırak |
| PATCH | `/api/admin/users/{id}/activate` | Kullanıcıyı aktifleştir |

## Kullanım

### Kayıt Ol
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "username": "johndoe", "password": "SecurePass123"}'
```

### Giriş Yap
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "SecurePass123"}'
```

### Korumalı Endpoint'e Erişim
```bash
curl http://localhost:8000/api/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Testler

```bash
pytest tests/ -v
```

## Docker

```bash
docker build -t auth-service .
docker run -p 8000:8000 auth-service
```

## API Dokümantasyonu

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
