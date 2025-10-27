# storage/cursor_state_store.py
import json
from pathlib import Path


CURSOR_PATH = Path(__file__).parent / "cursor_state.json"


class CursorStateStore:
    @staticmethod
    def load() -> str | None:
        if CURSOR_PATH.exists():
            data = json.loads(CURSOR_PATH.read_text())
            return data.get("last_cursor")
        return None

    @staticmethod
    def save(cursor: str | None) -> None:
        CURSOR_PATH.write_text(json.dumps({"last_cursor": cursor}, indent=2))
