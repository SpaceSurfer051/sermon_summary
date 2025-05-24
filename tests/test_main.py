import pytest
from fastapi import UploadFile
from io import BytesIO

def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    assert "설교 요약 API" in response.json()["message"]

def test_summarize_endpoint_with_valid_file(client, sample_text):
    # 텍스트 파일 생성
    file_content = BytesIO(sample_text.encode())
    files = {"file": ("test.txt", file_content, "text/plain")}
    
    response = client.post("/summarize", files=files)
    assert response.status_code == 200
    assert "status" in response.json()
    assert "summary" in response.json()
    assert response.json()["status"] == "success"

def test_summarize_endpoint_without_file(client):
    response = client.post("/summarize")
    assert response.status_code == 422  # Validation Error

def test_summarize_endpoint_with_empty_file(client):
    # 빈 파일 생성
    file_content = BytesIO(b"")
    files = {"file": ("empty.txt", file_content, "text/plain")}
    
    response = client.post("/summarize", files=files)
    assert response.status_code == 500  # Internal Server Error
    assert "status" in response.json()
    assert response.json()["status"] == "error" 