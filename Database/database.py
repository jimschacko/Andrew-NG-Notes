from __future__ import annotations

import json
from dataclasses import asdict
from datetime import date
from pathlib import Path
from typing import Any, Dict, Optional

from .base_database import BaseDatabase, RecordKey


class JsonFileDatabase(BaseDatabase):
    """Simple JSON file store for demo/testing purposes.

    Data model:
    {
      "platform|soul_id|YYYY-MM-DD": { ... data ... }
    }
    """

    def __init__(self, file_path: Path | str = "data.json") -> None:
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists():
            self._write({})

    def _read(self) -> Dict[str, Any]:
        try:
            raw = self.file_path.read_text(encoding="utf-8")
            return json.loads(raw or "{}")
        except FileNotFoundError:
            return {}

    def _write(self, data: Dict[str, Any]) -> None:
        self.file_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    @staticmethod
    def _key_to_str(key: RecordKey) -> str:
        day_str = key.day.isoformat()
        soul = key.soul_id if key.soul_id is not None else "__PUBLIC__"
        return f"{key.platform}|{soul}|{day_str}"

    def upsert(self, *, key: RecordKey, data: Dict[str, Any]) -> None:
        store = self._read()
        k = self._key_to_str(key)
        store[k] = data
        self._write(store)

    def get(self, *, key: RecordKey) -> Optional[Dict[str, Any]]:
        store = self._read()
        return store.get(self._key_to_str(key))

