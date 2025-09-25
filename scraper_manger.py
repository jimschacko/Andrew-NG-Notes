from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Sequence, Type

from scrape.base_scrape import BaseScraper, ScrapeTask, parse_date_range
from scrape.linkdin_scrape import LinkedInScraper
from scrape.codefed_scrope import CodefedScraper
from Database.base_database import RecordKey


@dataclass
class ScrapeConfig:
    date: Sequence[object]
    soul_ids: List[str]
    scrape_type: List[str]
    OverRide: bool


class ScraperManager:
    def __init__(self, *, scrapers: Iterable[Type[BaseScraper]]) -> None:
        self.scraper_classes: Dict[str, Type[BaseScraper]] = {}
        for cls in scrapers:
            if not cls.SCRAPER_KEY:
                continue
            self.scraper_classes[cls.SCRAPER_KEY] = cls

    def run(self, *, config: ScrapeConfig) -> List[ScrapeTask]:
        start_end = parse_date_range(config.date)
        results: List[ScrapeTask] = []
        for key in config.scrape_type:
            cls = self.scraper_classes.get(key)
            if cls is None:
                continue
            scraper = cls(override=config.OverRide)
            results.extend(scraper.scrape(date_range=start_end, soul_ids=config.soul_ids))
        return results

    @staticmethod
    def to_record_key(task: ScrapeTask) -> RecordKey:
        return RecordKey(platform=task.platform, soul_id=task.soul_id, day=task.day)


def create_default_manager() -> ScraperManager:
    return ScraperManager(scrapers=[LinkedInScraper, CodefedScraper])

