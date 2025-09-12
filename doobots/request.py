from doobots.base_message import BaseMessage

class Request(BaseMessage):
    def __init__(self, data: dict = {}, files: list[dict] = []):
        super().__init__(data, files)