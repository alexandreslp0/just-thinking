import pytest
from app import schemas


@pytest.mark.parametrize("post_id, content", [
    (1, "awesome post"),
    (2, "i like it!"),
    (1, "i read again and dont think it's awesome")
])
def test_successful_create_comment(authorized_client, test_user, test_posts, post_id, content):
    res_create_comment = authorized_client.post(
        f"/comments/{post_id}",
        json={"content": content}
    )

    comment = schemas.CommentFullResponse(**res_create_comment.json())
    assert res_create_comment.status_code == 201
    assert res_create_comment.json()["owner_id"] == test_user["id"]
    assert res_create_comment.json()["post_id"] == post_id


def test_post_not_found_create_comment(authorized_client, test_posts):
    res_create_comment = authorized_client.post(
        "/comments/9999999",
        json={"content": "my comment on post"}
    )
    assert res_create_comment.status_code == 404


def test_unauthorized_create_comment(client, test_posts):
    res_create_comment = client.post(
        f"/comments/{test_posts[0].id}",
        json={"content": "my comment on post"}
    )
    assert res_create_comment.status_code == 401


@pytest.mark.parametrize("id", [
    (1), # my post and my comment
    (3), # my post and other user comment
    (6)  # other user post and my comment
])
def test_successful_delete_comment(authorized_client, test_comments, id):
    res_delete_comment = authorized_client.delete(f"/comments/{id}")
    assert res_delete_comment.status_code == 204


def test_wrong_owner_and_postowner_delete_comment(authorized_client, test_comments):
    res_delete_comment = authorized_client.delete(f"/comments/{test_comments[4].id}")
    assert res_delete_comment.status_code == 403


def test_unauthorized_delete_comment(client, test_comments):
    res_delete_comment = client.delete(f"/comments/{test_comments[0].id}")
    assert res_delete_comment.status_code == 401


def test_not_found_delete_comment(authorized_client, test_comments):
    res_delete_comment = authorized_client.delete(f"/comments/999999999")
    assert res_delete_comment.status_code == 404
