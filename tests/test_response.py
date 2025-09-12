import os
import pytest
from doobots import Response

def test_response_put_and_files():
    response = Response()
    response.put("key1", "value1")
    response.put_file(file_name="test.txt", base64="dGVzdA==")
    
    with open("teste_doobots_python_response.txt", "w") as f:
        f.write("teste")
    
    response.put_file(file_path="teste_doobots_python_response.txt")
    os.remove("teste_doobots_python_response.txt")

    assert len(response.get_files()) == 2
    assert response.get("key1") == "value1"
    assert response.get("non_existent_key") is None
    assert response.get("non_existent_key", "default") == "default"
    assert response.get_file("test.txt") is not None
    assert response.get_file("non_existent_file.txt") is None
    assert response.get_file("test.txt").fileName == "test.txt"
    assert response.get_file("test.txt").base64 == "dGVzdA=="
    assert response.get_file("teste_doobots_python_response.txt") is not None
    
    out = response.to_dict()
    data = out["data"]
    assert data is not None
    files = out["files"]
    assert files is not None
    assert isinstance(files, list)
    
    assert data["key1"] == "value1"
    assert any(f["fileName"] == "test.txt" for f in files)
    assert any(f["fileName"] == "teste_doobots_python_response.txt" for f in files)

    with pytest.raises(TypeError):
        response.put(123, "value")
    with pytest.raises(TypeError):
        response.put_all("not a dict")
    with pytest.raises(ValueError):
        response.put_json("invalid json")
    with pytest.raises(ValueError):
        response.put_file()
    with pytest.raises(FileNotFoundError):
        response.put_file(file_path="non_existent_file.txt")
    with pytest.raises(TypeError):
        response.put_file(file_name=123, base64="dGVzdA==")
    with pytest.raises(TypeError):
        response.put_file(file_name="test.txt", base64=123)
    with pytest.raises(TypeError):
        response.put_file(file_path=123)
