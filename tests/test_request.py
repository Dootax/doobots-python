from doobots import Request

def test_request_get_and_files():
    input_data = {
        "name": "Matheus",
        "files": [{"fileName": "test.txt", "base64": "dGVzdA=="}]
    }
    req = Request(input_data)
    assert req.get("name") == "Matheus"
    f = req.get_file("test.txt")
    assert f["base64"] == "dGVzdA=="
    assert req.get_file("nonexistent") is None
