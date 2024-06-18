from database.orm import ToDo

def test_health_check(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_todos(client, mocker):
    mocker.patch("main.get_todos", return_value=[
        ToDo(id=1, contents="test", is_done=True),
        ToDo(id=2, contents="test", is_done=False),
    ])
    response = client.get("/todos")
    assert response.status_code == 200
    assert response.json() == {
        "todos":[
            {"id": 1, "contents": "test", "is_done":True},
            {"id": 2, "contents": "test", "is_done":False},
        ]
    }
    
    # desc
    response = client.get("/todos?order=desc")
    assert response.status_code == 200
    assert response.json() == {
        "todos":[
            {"id": 2, "contents": "test", "is_done":False},
            {"id": 1, "contents": "test", "is_done":True},
        ]
    }
    
    
def test_get_todo(client, mocker):
    # 200
    mocker.patch("main.get_todo_by_todo_id", return_value=ToDo(id=1, contents="test", is_done=True),)
    response = client.get("/todos/1")
    assert response.status_code == 200
    assert response.json() ==  {"id": 1, "contents": "test", "is_done":True}
    
    # 404
    mocker.patch("main.get_todo_by_todo_id", return_value=None)
    response = client.get("/todos/1")
    assert response.status_code == 404
    assert response.json() ==  {"detail": "ToDo Not Found"}
    
def test_create_todo(client, mocker):
    create_spy = mocker.spy(ToDo, "create")
    mocker.patch("main.create_todo", return_value=ToDo(id=1, contents="test11", is_done=False),)
    
    body = {
        "contents": "test",
        "is_done": False,
    }
    response = client.post("/todos", json=body)
    
    assert create_spy.spy_return.id is None
    assert create_spy.spy_return.contents == "test"
    assert create_spy.spy_return.is_done is False
    
    assert response.status_code == 201
    assert response.json() ==  {"id": 1, "contents": "test11", "is_done":False}
  
def test_update_todo(client, mocker):
    # 200
    mocker.patch("main.get_todo_by_todo_id", return_value=ToDo(id=1, contents="test", is_done=True),)
    undone = mocker.patch.object(
        ToDo, "undone"
    )
    mocker.patch("main.update_todo", return_value=ToDo(id=1, contents="test", is_done=False),)

    response = client.patch("/todos/1", json={"is_done": False})
    
    undone.assert_called_once_with()
    assert response.status_code == 200
    assert response.json() ==  {"id": 1, "contents": "test", "is_done":False}
    
    # 404
    mocker.patch("main.get_todo_by_todo_id", return_value=None)
    response = client.patch("/todos/1", json={"is_done": False})
    assert response.status_code == 404
    assert response.json() ==  {"detail": "ToDo Not Found"}
    
    
def test_delete_todo(client, mocker):
    # 204
    mocker.patch("main.get_todo_by_todo_id", return_value=ToDo(id=1, contents="test", is_done=True),)
    mocker.patch("main.delete_todo", return_value=None)
    response = client.delete("/todos/1")
    assert response.status_code == 204
    
    # 404
    mocker.patch("main.get_todo_by_todo_id", return_value=None)
    response = client.get("/todos/1")
    assert response.status_code == 404
    assert response.json() ==  {"detail": "ToDo Not Found"}