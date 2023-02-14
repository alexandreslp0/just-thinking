from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app import models
from app.oauth2 import create_access_token
from app.main import app
from app.config import settings
from app.database import get_db
from app.database import Base

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_host}:\
    {settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
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
def test_user(client):
    user_data = {"email": "test@user.com", "password": "senhateste"}
    res = client.post("/users", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def test_user2(client):
    user_data = {"email": "test2@email.com", "password": "test1234"}
    res = client.post("/users", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    
    return client


@pytest.fixture
def test_posts(session, test_user, test_user2):
    posts_data = [
        {"title": "title post 1", "content": "content post 1", "published": True, "owner_id": test_user["id"]},
        {"title": "title post 2", "content": "xpto body", "published": False, "owner_id": test_user["id"]},
        {"title": "title post 3", "content": "this is a post content", "published": True, "owner_id": test_user2["id"]},
        {"title": "title post 4", "content": "my other post", "published": True, "owner_id": test_user["id"]}
    ]

    def validate_post_schema(post):
        return models.PostTable(**post)

    posts = list(map(validate_post_schema, posts_data))

    session.add_all(posts)
    session.commit()

    get_posts = session.execute(text("SELECT * FROM posts")).mappings().all()

    return get_posts


@pytest.fixture
def test_comments(session, test_user, test_user2, test_posts):
    comments_data = [
        {"content": "comment 1 in post 1", "post_id": test_posts[0].id, "owner_id": test_user["id"]},
        {"content": "comment 2 in post 1", "post_id": test_posts[0].id, "owner_id": test_user["id"]},
        {"content": "comment 3 in post 1", "post_id": test_posts[0].id, "owner_id": test_user2["id"]},
        {"content": "comment 1 in post 2", "post_id": test_posts[1].id, "owner_id": test_user["id"]},
        {"content": "comment 1 in post 3", "post_id": test_posts[2].id, "owner_id": test_user2["id"]},
        {"content": "comment 2 in post 3", "post_id": test_posts[2].id, "owner_id": test_user["id"]},
    ]

    def validate_comment_schema(comment):
        return models.CommentsTable(**comment)

    comments = list(map(validate_comment_schema, comments_data))

    session.add_all(comments)
    session.commit()

    get_comments = session.execute(text("SELECT * FROM comments")).mappings().all()

    return get_comments