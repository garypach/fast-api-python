import json
from tests.conftest import authorized_client, test_posts, test_user


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    print(res.json())
    assert res.status_code == 200

def test_get_one_posts(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 200

def test_unauthorized_user_get_posts(client,test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401

def test_unauthorized_user_get_one_post(client,test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def create_post(authorized_client,test_user,test_posts):
    res = authorized_client.post(f"/posts/", json = {"title":'test title1',"content":"test content1","published":True})
    assert res.status_code == 201

def test_unauthorized_user_create_posts(client,test_posts):
    res = client.post(f"/posts/", json = {"title":'test title1',"content":"test content1","published":True})
    assert res.status_code == 401

def test_unauthorized_user_delete_posts(client,test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_user_delete_posts(authorized_client,test_user,test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_other_user_posts(authorized_client,test_user,test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

def test_update_posts(authorized_client,test_user,test_posts):
    data={
        "title":"new title",
        "content":"new content",
        "id":test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}" , json= data)
    assert res.status_code == 200