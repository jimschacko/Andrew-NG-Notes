from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Dict, Iterable, List, Optional, Tuple


DateRange = Tuple[date, date]


def _parse_date(value: Any) -> date:
    if isinstance(value, date):
        return value
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, str):
        # Accept ISO formats like YYYY-MM-DD, or full ISO datetime
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
        except ValueError:
            pass
    raise ValueError(f"Unsupported date value: {value!r}")


def parse_date_range(raw_range: Iterable[Any]) -> DateRange:
    values = list(raw_range)
    if len(values) != 2:
        raise ValueError("date must be a pair: [start_date, end_date]")
    start = _parse_date(values[0])
    end = _parse_date(values[1])
    if end < start:
        raise ValueError("end_date must be on/after start_date")
    return start, end


@dataclass(frozen=True)
class ScrapeTask:
    platform: str
    soul_id: Optional[str]
    day: date
    data: Dict[str, Any]


class BaseScraper(ABC):
    """Abstract base class for all scrapers.

    Subclasses must implement the scrape method and set SCRAPER_KEY to
    the value expected in the input "scrape_type" list.
    """

    SCRAPER_KEY: str = ""  # e.g., "Linkdin" or "codechef" as provided in config

    def __init__(self, *, override: bool = False) -> None:
        self.override = override

    @abstractmethod
    def scrape(
        self,
        *,
        date_range: DateRange,
        soul_ids: List[str],
    ) -> List[ScrapeTask]:
        """Perform scrape and return list of ScrapeTask results.

        - If soul_ids is empty, the scraper may choose a default behavior
          (e.g., scrape trending/public data).
        - The caller is responsible for persisting via the database layer.
        """
        raise NotImplementedError

