from __future__ import annotations

from datetime import timedelta
from typing import List

from .base_scrape import BaseScraper, ScrapeTask, DateRange


class CodefedScraper(BaseScraper):
    # Map to user's key for CodeChef in input
    SCRAPER_KEY = "codechef"

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
                results.append(
                    ScrapeTask(
                        platform=self.SCRAPER_KEY,
                        soul_id=None,
                        day=current,
                        data={
                            "summary": "Sample CodeChef daily summary",
                            "contests": 0,
                            "problems_solved": 0,
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
                                "handle": sid,
                                "rating": None,
                                "problems_solved": 0,
                                "override": self.override,
                            },
                        )
                    )
            current += timedelta(days=1)
        return results

