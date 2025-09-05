import os
from doobots import Response

def test_response_put_and_files():
    r = Response()
    r.put("key1", "value1")
    r.put_file(file_name="test.txt", base64="dGVzdA==")
    
    with open("/tmp/teste_doobots_python_response.txt", "w") as f:
        f.write("teste")
    
    r.put_file(file_path="/tmp/teste_doobots_python_response.txt")
    os.remove("/tmp/teste_doobots_python_response.txt")
    
    out = r.to_dict()
    assert out["key1"] == "value1"
    assert any(f["fileName"] == "test.txt" for f in out["files"])
    assert any(f["fileName"] == "teste_doobots_python_response.txt" for f in out["files"])
