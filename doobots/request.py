class Request:
    def __init__(self, data: dict):
        self._data = dict(data)
        self._files = data.get("files", [])

    def get(self, key, default_value=None):
        return self._data.get(key, default_value)
    
    def to_dict(self):
        return self._data
    
    def get_files(self):
        return self._files

    def get_file(self, file_name):
        for f in self._files:
            if f.get("fileName") == file_name:
                return f
        return None
