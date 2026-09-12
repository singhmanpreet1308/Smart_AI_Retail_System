#!/usr/bin/env python3

"""Find Argos prices using the shared browser retailer workflow."""

import asyncio
from pathlib import Path

import test_currys as retailer_engine


# Configure the shared exact-model discovery and price extraction workflow.
retailer_engine.RETAILER = "Argos"
retailer_engine.RETAILER_DOMAIN = "argos.co.uk"
retailer_engine.SEARCH_SITE_PATH = "argos.co.uk/product"
retailer_engine.CACHE_FILE = Path("argos_urls.json")


if __name__ == "__main__":
    raise SystemExit(
        asyncio.run(retailer_engine.main())
    )
