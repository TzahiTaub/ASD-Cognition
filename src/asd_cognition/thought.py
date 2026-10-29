from datetime import datetime as dt


def encode(val: int, n_bytes):
    return val.to_bytes(n_bytes, "little")


class EncodingSizes:
    USER_ID = 8
    TIMESTAMP = 8
    THOUGHT_SIZE = 4


TIMESTAMP_OFFSET = EncodingSizes.USER_ID
THOUGHT_SIZE_OFFSET = TIMESTAMP_OFFSET + EncodingSizes.TIMESTAMP
THOUGHT_OFFSET = THOUGHT_SIZE_OFFSET + EncodingSizes.THOUGHT_SIZE


class Thought:
    def __init__(self, user_id: int, timestamp: dt, thought: str):
        self.user_id = user_id
        self.timestamp = timestamp
        self.thought = thought

    def __repr__(self):
        user_id, timestamp, thought = self.user_id, self.timestamp, self.thought
        return f"Thought({user_id=}, {timestamp=}, {thought=})"

    def __str__(self):
        ts_str = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return f"[{ts_str}] user {self.user_id}: {self.thought}"

    def __eq__(self, value):
        if not isinstance(value, Thought):
            return False
        return self.__dict__ == value.__dict__

    def serialize(self):
        ts = int(self.timestamp.timestamp())
        header = b"".join(map(encode, (self.user_id, ts, len(self.thought)), (8, 8, 4)))
        return header + self.thought.encode()

    @classmethod
    def deserialize(cls, data: bytes):
        view = memoryview(data)
        user_id = int.from_bytes(view[:TIMESTAMP_OFFSET], "little")
        ts = int.from_bytes(view[TIMESTAMP_OFFSET:THOUGHT_SIZE_OFFSET], "little")
        thought = data[THOUGHT_OFFSET:].decode()
        return cls(user_id, dt.fromtimestamp(ts), thought)
