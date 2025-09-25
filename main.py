from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List

from scraper_manger import ScrapeConfig, create_default_manager
from Database.database import JsonFileDatabase


def load_config(path: str | Path) -> Dict[str, Any]:
    text = Path(path).read_text(encoding="utf-8")
    return json.loads(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run scrapers with a JSON config file.")
    parser.add_argument("config", type=str, help="Path to config JSON file")
    parser.add_argument("--out", type=str, default="data/data.json", help="Output JSON DB path")
    args = parser.parse_args()

    raw = load_config(args.config)

    config = ScrapeConfig(
        date=raw.get("date", []),
        soul_ids=raw.get("soul_ids", []),
        scrape_type=raw.get("scrape_type", []),
        OverRide=bool(raw.get("OverRide", False)),
    )

    manager = create_default_manager()
    tasks = manager.run(config=config)

    db = JsonFileDatabase(args.out)
    for task in tasks:
        key = manager.to_record_key(task)
        db.upsert(key=key, data=task.data)

    print(f"Wrote {len(tasks)} records to {args.out}")


if __name__ == "__main__":
    main()

