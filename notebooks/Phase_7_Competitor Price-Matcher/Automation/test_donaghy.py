#!/usr/bin/env python3

"""Find Donaghy Bros prices using the shared retailer workflow."""

import asyncio
from pathlib import Path

import test_currys as retailer_engine


# Search the full domain because Donaghy Bros product paths can vary.
# The shared engine still requires the exact normalized model in each result.
retailer_engine.RETAILER = "Donaghy Bros"
retailer_engine.RETAILER_DOMAIN = "donaghybros.co.uk"
retailer_engine.SEARCH_SITE_PATH = "donaghybros.co.uk"
retailer_engine.CACHE_FILE = Path("donaghy_urls.json")


if __name__ == "__main__":
    raise SystemExit(
        asyncio.run(retailer_engine.main())
    )
