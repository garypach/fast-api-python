from jose import jwt
import pytest
from app import schemas
from app.config import settings


def test_create_user(client):
    res = client.post("/users/", json={
    "email":"hello2@gmail.com",
    "password":"123"
    })
    assert res.status_code == 201

def test_login_user(client,test_user):
    res = client.post("/login", data={
    "username":test_user['email'],
    "password":test_user['password']    
    })
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=settings.algorithm)
    id:str = payload.get("user_id")
    assert id == test_user['id']
    assert res.status_code == 200

def test_login_user_error(client,test_user):
    res = client.post("/login", data={
    "username":test_user['email'],
    "password":'password'
    })
    assert res.status_code == 403

