from fastapi.testclient import TestClient
from app.main import app
from app.routers import get_db
from app.schemas import TaskCreate, Task

def temp_db(f):
    def func(SessionLocal, *args, **kwargs):
        # テスト用のDBに接続するためのsessionmaker instanse
        #  (SessionLocal) をfixtureから受け取る

        def override_get_db():
            try:
                db = SessionLocal()
                yield db
            finally:
                db.close()

        # fixtureから受け取るSessionLocalを使うようにget_dbを強制的に変更
        app.dependency_overrides[get_db] = override_get_db
        # Run tests
        f(*args, **kwargs)
        # get_dbを元に戻す
        app.dependency_overrides[get_db] = get_db
    return func

client = TestClient(app)

@temp_db
def test_get_tasks():
    response = client.get("/task")
    assert response.status_code == 200
    assert response.json() == []

@temp_db
def test_create_task():
    data = TaskCreate(title="test")
    response = client.post("/task", json=dict(data))
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "test", "is_done": False}

@temp_db
def test_toggle_task():
    data = TaskCreate(title="test")
    client.post("/task", json=dict(data))
    response = client.put("/task/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "test", "is_done": True}

@temp_db
def test_delete_task():
    data = TaskCreate(title="test")
    client.post("/task", json=dict(data))
    response = client.delete("/task/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "test", "is_done": False}