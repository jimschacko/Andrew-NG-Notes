from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from typing import Any, Dict, Iterable, Optional


@dataclass(frozen=True)
class RecordKey:
    platform: str
    soul_id: Optional[str]
    day: date


class BaseDatabase(ABC):
    @abstractmethod
    def upsert(self, *, key: RecordKey, data: Dict[str, Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(self, *, key: RecordKey) -> Optional[Dict[str, Any]]:
        raise NotImplementedError

    def bulk_upsert(self, items: Iterable[tuple[RecordKey, Dict[str, Any]]]) -> None:
        for key, data in items:
            self.upsert(key=key, data=data)

