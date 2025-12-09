from fastapi.testclient import TestClient
from app.main import app
from app.dependencies import get_db
import pytest
import io

client = TestClient(app)



def test_get_file_endpoint(mocker):
    mock_db = mocker.Mock() #Mocking the db and the file with mock class.
    mock_file = mocker.Mock()
    
    mock_file.id = 1
    mock_file.body = b"Body"
    mock_file.type = "text/plain"
    mock_file.file_name ="Test.txt"
    #We establish the parameters for the mocked file.

    def mock_get(model, file_id): #Mocking the same as file = db.get(Files, file_id)
        if file_id == 1:
            return mock_file
        return None
    
    mock_db.get.side_effect = mock_get

    def db_override(): 
        yield mock_db
    app.dependency_overrides[get_db] = db_override #Overriding the db dependency with the mock db

    response = client.get("/files/1")
    assert response.status_code == 200
    assert response.content == b"Body"
    assert response.headers["content-disposition"] == 'attachment; filename="Test.txt"'

    response = client.get("/files/200000")
    assert response.status_code == 404
    assert response.json() == {"detail":"File not found"}
    app.dependency_overrides.clear()

def test_upload_file_endpoint(mocker):
    mock_db = mocker.Mock()

    def db_override(): 
        yield mock_db

    app.dependency_overrides[get_db] = db_override

    file_content = b"test"
    test_file = io.BytesIO(file_content)

    response = client.post("/upload",
                           files={"uploaded_file": ("test.txt", test_file, "text/plain")})

    assert response.status_code == 201
    assert response.json() == {"message":"File uploaded successfully"}
    app.dependency_overrides.clear()

def test_upload_file_endpoint_invalid_type(mocker):
    mock_db = mocker.Mock()

    def db_override():
        yield mock_db

    app.dependency_overrides[get_db] = db_override

    file_content = b"\x89PNG\r\n\x1a\n"
    test_file = io.BytesIO(file_content)

    response = client.post(
        "/upload",
        files={"uploaded_file": ("image.png", test_file, "image/png")}
    )

    assert response.status_code == 415
    assert response.json() == {"detail": "File type not supported."}

    app.dependency_overrides.clear()