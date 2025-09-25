from __future__ import annotations

from datetime import timedelta
from typing import List

from .base_scrape import BaseScraper, ScrapeTask, DateRange


class LinkedInScraper(BaseScraper):
    # Match user-provided key exactly to avoid confusion
    SCRAPER_KEY = "Linkdin"

    def scrape(
        self,
        *,
        date_range: DateRange,
        soul_ids: List[str],
    ) -> List[ScrapeTask]:
        start, end = date_range
        results: List[ScrapeTask] = []
        current = start
        while current <= end:
            if not soul_ids:
                # Example public/trending placeholder
                results.append(
                    ScrapeTask(
                        platform=self.SCRAPER_KEY,
                        soul_id=None,
                        day=current,
                        data={
                            "summary": "Sample LinkedIn summary",
                            "posts": 0,
                            "override": self.override,
                        },
                    )
                )
            else:
                for sid in soul_ids:
                    results.append(
                        ScrapeTask(
                            platform=self.SCRAPER_KEY,
                            soul_id=sid,
                            day=current,
                            data={
                                "profile": sid,
                                "connections": 0,
                                "posts": 0,
                                "override": self.override,
                            },
                        )
                    )
            current += timedelta(days=1)
        return results

