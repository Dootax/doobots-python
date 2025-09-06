import json
import base64 as base64tools
import os
from doobots.file import File

class Response:
    def __init__(self):
        self._data : dict = {}
        self._files: list[File] = []

    def put(self, key: str, value: any):
        self._data[key] = value

    def put_all(self, d: dict):
        self._data.update(d)

    def put_json(self, json_str: str):
        try:
            obj = json.loads(json_str)
            if isinstance(obj, dict):
                self._data.update(obj)
        except Exception as e:
            raise ValueError(f"Invalid JSON: {e}")

    def put_file(self, file_name=None, base64=None, file_path=None):
        if file_path:
            if not os.path.isfile(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
            file_name = os.path.basename(file_path)
            with open(file_path, "rb") as f:
                base64 = base64tools.b64encode(f.read()).decode("utf-8")
        if not file_name or not base64:
            raise ValueError("Either file_name+base64 or file_path must be provided")
        
        self._files.append(File(base64, file_name))

    def to_dict(self) -> dict:
        return {
            "data": self._data,
            "files": self._files
        }
