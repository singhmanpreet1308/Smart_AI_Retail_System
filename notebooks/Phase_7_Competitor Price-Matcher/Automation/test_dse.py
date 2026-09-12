#!/usr/bin/env python3

"""Find Dominic Smith Electrical (DSE) product prices."""

import asyncio
from pathlib import Path

import test_currys as retailer_engine


# Search the full retailer domain; exact normalized model matching in the
# shared engine prevents unrelated search results from being selected.
retailer_engine.RETAILER = "DSE"
retailer_engine.RETAILER_DOMAIN = "dominicsmithelectrical.co.uk"
retailer_engine.SEARCH_SITE_PATH = "dominicsmithelectrical.co.uk"
retailer_engine.CACHE_FILE = Path("dse_urls.json")


if __name__ == "__main__":
    raise SystemExit(
        asyncio.run(retailer_engine.main())
    )
