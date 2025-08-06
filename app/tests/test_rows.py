from fastapi.testclient import TestClient
import main

client = TestClient(main.app)

def test_read_rows(monkeypatch):
    class DummyDF:
        def to_dict(self, orient):
            return[{"col": "val"}]
    
    class DummyCursor:
        def execute(self, sql):
            return DummyDF()
        
    class DummyConn:
        def cursor(self):
            return DummyCursor()
        
    monkeypatch.setattr("services.athena.get_athena_conn", lambda: DummyConn())

    response = client.get("/rows?limit=1")
    assert response.status_code == 200
    assert response.json() == [{"col": "val"}]
    