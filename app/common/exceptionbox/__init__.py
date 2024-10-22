class BasicException(Exception):
    def __init__(self, msg: str, code: int = 500) -> None:
        self.msg = msg
