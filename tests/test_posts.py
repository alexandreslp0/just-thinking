import pytest
from app import schemas


def test_successful_get_posts(authorized_client, test_posts):
    res_get_posts = authorized_client.get("/posts")

    def validate_schema(post):
        return schemas.PostFullResponse(**post)

    posts = list(map(validate_schema, res_get_posts.json()))
    assert len(test_posts) == len(posts)
    assert res_get_posts.status_code == 200


def test_unauthorized_get_posts(client, test_posts):
    res_get_posts = client.get("/posts")
    assert res_get_posts.status_code == 401


def test_successful_get_post(authorized_client, test_posts):
    res_get_posts = authorized_client.get(f"/posts/{test_posts[0].id}") 
    post = schemas.PostFullResponse(**res_get_posts.json())
    assert res_get_posts.status_code == 200

def test_not_found_get_post(authorized_client, test_posts):
    res_get_posts = authorized_client.get(f"/posts/999999999")
    assert res_get_posts.status_code == 404

def test_unauthorized_get_post(client, test_posts):
    res_get_posts = client.get(f"/posts/{test_posts[0].id}")
    assert res_get_posts.status_code == 401


@pytest.mark.parametrize("title, content, published", [
    ("title test 1", "content test 1", True),
    ("title test 2", "content test 2", False),
    ("title test 3", "content test 3", True)
])
def test_successful_create_post(authorized_client, test_user, title, content, published):
    res_create_post = authorized_client.post(
        "/posts",
        json={"title": title, "content": content, "published": published}
    )

    post = schemas.PostCreateResponse(**res_create_post.json())
    assert res_create_post.status_code == 201
    assert res_create_post.json()["owner"]["id"] == test_user["id"]


def test_default_published_create_post(authorized_client, test_user):
    res_create_post = authorized_client.post(
        "/posts",
        json={"title": "some title", "content": "some content"}
    )

    post = schemas.PostCreateResponse(**res_create_post.json())
    assert res_create_post.status_code == 201
    assert res_create_post.json()["owner"]["id"] == test_user["id"]
    assert res_create_post.json()["published"] == True


def test_invalid_field_create_post(authorized_client, test_user):
    res_create_post = authorized_client.post(
        "/posts",
        json={"this_field_is_invalid": "some title", "content": "some content"}
    )

    assert res_create_post.status_code == 422


def test_unauthorized_create_post(client, test_user):
    res_create_post = client.post(
        "/posts",
        json={"title": "some title", "content": "some content"}
    )

    assert res_create_post.status_code == 401


def test_successul_delete_post(authorized_client, test_user, test_posts):
    res_delete_post = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res_delete_post.status_code == 204


def test_wrong_user_delete_post(authorized_client, test_user, test_posts):
    res_delete_post = authorized_client.delete(f"/posts/{test_posts[2].id}")
    assert res_delete_post.status_code == 403


def test_unauthorized_delete_post(client, test_posts):
    res_delete_post = client.delete(f"/posts/{test_posts[0].id}")
    assert res_delete_post.status_code == 401


def test_not_found_delete_post(authorized_client, test_posts):
    res_delete_post = authorized_client.delete(f"/posts/999999999")
    assert res_delete_post.status_code == 404


@pytest.mark.parametrize("id, title, content, published", [
    (1, "new title", "new content", False),
    (1, "some other title", "new content", False),
    (1, "some other title", "new content", True),
    (4, "title test 3", "content test 3", True)
])
def test_successful_update_post(authorized_client, test_posts, test_user, id, title, content, published):
    res_update_post = authorized_client.put(
        f"/posts/{id}",
        json={"title": title, "content": content, "published": published}
    )

    post = schemas.PostCreateResponse(**res_update_post.json())
    assert res_update_post.status_code == 200
    assert res_update_post.json()["title"] == title
    assert res_update_post.json()["content"] == content
    assert res_update_post.json()["published"] == published


def test_invalid_field_update_post(authorized_client, test_posts):
    res_update_post = authorized_client.put(
        f"/posts/{test_posts[0].id}",
        json={"this_field_is_invalid": "some title", "content": "some content"}
    )

    assert res_update_post.status_code == 422


def test_unauthorized_update_post(client, test_posts):
    res_create_post = client.put(
        f"/posts/{test_posts[0].id}",
        json={"title": "some title", "content": "some content", "published": "true"}
    )

    assert res_create_post.status_code == 401


def test_wrong_user_update_post(authorized_client, test_posts):
    res_delete_post = authorized_client.put(
        f"/posts/{test_posts[2].id}",
        json={"title": "new", "content": "try update this", "published": "true"}
    )
    assert res_delete_post.status_code == 403
