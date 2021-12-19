from fastapi.testclient import TestClient
from app.database import get_db,Base
from app.main import app
from app.config import settings
from app.oAuth2 import create_access_token
from app import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pytest

SQLALCHEMY_DATABASE_URL = (f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test")
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

Testing_SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = Testing_SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user2(client):
    user_data = {
    "email":"hello1@gmail.com",
    "password":"123"
    }
    res = client.post("/users/", json= user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user(client):
    user_data = {
    "email":"hello2@gmail.com",
    "password":"123"
    }
    res = client.post("/users/", json= user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization":f"Bearer {token}"
    }
    return client


@pytest.fixture
def test_posts(test_user,session,test_user2):
    post_data = [
        {
        "title":"title1",
        "content":"content1",
        "owner_id":test_user['id']
        },
         {
        "title":"title2",
        "content":"content2",
        "owner_id":test_user['id']
        },
         {
        "title":"title3",
        "content":"content3",
        "owner_id":test_user['id']
        },
          {
        "title":"title3",
        "content":"content3",
        "owner_id":test_user2['id']
        },
    ]
    def create_post_from_model(post):
       return models.Post(**post)

    post_map = map(create_post_from_model,post_data)

    posts = list((post_map))

    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()

    return posts