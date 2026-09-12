#!/usr/bin/env python3

"""Find Currys product prices for the models in SOA.xlsx."""

import asyncio
import json
import os
import random
import re
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

import openpyxl
import requests
from dotenv import load_dotenv
from playwright.async_api import async_playwright

from common import (
    INPUT_FILE,
    OUTPUT_FILE,
    get_or_create_workbook,
    update_retailer_cell,
)


load_dotenv()

RETAILER = "Currys"
RETAILER_DOMAIN = "currys.co.uk"
SEARCH_SITE_PATH = "currys.co.uk/products"
CACHE_FILE = Path("currys_urls.json")
SERPAPI_ENDPOINT = "https://serpapi.com/search.json"
SERPAPI_KEY = os.getenv("SERPAPI_KEY", "").strip()

HEADLESS = False
PAGE_TIMEOUT_MS = 60_000
WAIT_AFTER_LOAD_MS = 3_000
MAX_429_RETRIES = 3
MIN_PRODUCT_DELAY_SECONDS = 8
MAX_PRODUCT_DELAY_SECONDS = 15


def normalize(value):
    return re.sub(r"[^A-Z0-9]", "", str(value or "").upper())


def clean_product_url(url):
    """Keep the canonical product path and discard tracking parameters."""
    parts = urlsplit(str(url or ""))
    return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))


def parse_search_price(value):
    """Parse only explicitly labelled GBP prices from search data."""
    match = re.search(
        r"(?:£\s*|GBP\s*)([0-9]{1,4}(?:,[0-9]{3})*(?:\.[0-9]{2})?)",
        str(value or ""),
        flags=re.IGNORECASE,
    )
    if not match:
        return None
    return float(match.group(1).replace(",", ""))


def find_search_price(result):
    """Find an explicit GBP price in one exact Currys search result."""
    rich_snippet = result.get("rich_snippet", {})
    top = rich_snippet.get("top", {}) if isinstance(rich_snippet, dict) else {}
    detected = top.get("detected_extensions", {}) if isinstance(top, dict) else {}

    if isinstance(detected, dict):
        raw_price = detected.get("price")
        if isinstance(raw_price, (int, float)) and raw_price > 0:
            return float(raw_price)

    values = [
        result.get("snippet"),
        result.get("displayed_link"),
        top.get("extensions") if isinstance(top, dict) else None,
        detected,
    ]

    for value in values:
        price = parse_search_price(value)
        if price is not None:
            return price
    return None


def read_products(input_path=INPUT_FILE):
    workbook = openpyxl.load_workbook(input_path, data_only=True)
    worksheet = workbook.active
    products = []

    for row in worksheet.iter_rows(min_row=2, values_only=True):
        model = str(row[0] or "").strip() if row else ""
        description = str(row[1] or "").strip() if len(row) > 1 else ""
        if model:
            products.append({"model": model, "description": description})

    workbook.close()
    return products


def load_cache():
    try:
        data = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}


def save_cache(cache):
    CACHE_FILE.write_text(
        json.dumps(cache, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def discover_with_serpapi(model):
    """Return an exact retailer product URL and any search-listed price."""
    if not SERPAPI_KEY:
        print("    -> SERPAPI_KEY is missing")
        return None

    query = f'site:{SEARCH_SITE_PATH} "{model}"'
    print(f"    -> SerpApi search: {query}")

    try:
        response = requests.get(
            SERPAPI_ENDPOINT,
            params={
                "engine": "google",
                "q": query,
                "google_domain": "google.co.uk",
                "gl": "uk",
                "hl": "en",
                "num": 10,
                "api_key": SERPAPI_KEY,
            },
            timeout=30,
        )
        print(f"    -> SerpApi HTTP: {response.status_code}")
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError) as exc:
        print(f"    -> SerpApi failed: {exc}")
        return None

    if data.get("error"):
        print(f"    -> SerpApi error: {data['error']}")
        return None

    target = normalize(model)
    candidates = []

    for result in data.get("organic_results", []):
        link = clean_product_url(result.get("link", ""))
        title = str(result.get("title", ""))
        snippet = str(result.get("snippet", ""))
        combined = normalize(f"{link} {title} {snippet}")

        if RETAILER_DOMAIN not in link.lower() or target not in combined:
            continue

        score = 100
        if target in normalize(link):
            score += 200
        if target in normalize(title):
            score += 150
        candidates.append(
            {
                "score": score,
                "url": link,
                "price": find_search_price(result),
            }
        )

    if not candidates:
        print(f"    -> no exact {RETAILER} model result")
        return None

    candidates.sort(key=lambda item: item["score"], reverse=True)
    chosen = candidates[0]
    print(f"    -> discovered URL: {chosen['url']}")
    if chosen["price"] is not None:
        print(f"    -> search-listed price: £{chosen['price']:.2f}")
    return chosen


def parse_price(value):
    if isinstance(value, (int, float)) and value > 0:
        return float(value)

    match = re.search(
        r"(?:£|GBP\s*)?([0-9]{1,3}(?:,[0-9]{3})*(?:\.[0-9]{2})?)",
        str(value or ""),
        flags=re.IGNORECASE,
    )
    if not match:
        return None

    price = float(match.group(1).replace(",", ""))
    return price if price > 0 else None


def find_json_price(value):
    """Recursively find a Product/Offer price in JSON-LD."""
    if isinstance(value, list):
        for item in value:
            price = find_json_price(item)
            if price is not None:
                return price
        return None

    if not isinstance(value, dict):
        return None

    value_type = value.get("@type", "")
    types = value_type if isinstance(value_type, list) else [value_type]
    is_product_data = any(
        str(item).lower() in {"product", "offer", "aggregateoffer"}
        for item in types
    )

    if is_product_data:
        for key in ("price", "lowPrice", "highPrice"):
            price = parse_price(value.get(key))
            if price is not None:
                return price

        price = find_json_price(value.get("offers"))
        if price is not None:
            return price

    for child in value.values():
        if isinstance(child, (dict, list)):
            price = find_json_price(child)
            if price is not None:
                return price

    return None


async def extract_price(page):
    for script in await page.locator('script[type="application/ld+json"]').all():
        try:
            price = find_json_price(json.loads(await script.text_content() or ""))
            if price is not None:
                print(f"    -> JSON-LD price: £{price:.2f}")
                return price
        except (json.JSONDecodeError, TypeError):
            continue

    selectors = (
        'meta[property="product:price:amount"]',
        'meta[property="og:price:amount"]',
        'meta[itemprop="price"]',
        '[itemprop="price"]',
        '[data-product-price]',
        '[data-price]',
    )

    for selector in selectors:
        locator = page.locator(selector).first
        if not await locator.count():
            continue
        for value in (
            await locator.get_attribute("content"),
            await locator.get_attribute("data-price"),
            await locator.text_content(),
        ):
            price = parse_price(value)
            if price is not None:
                print(f"    -> page price: £{price:.2f}")
                return price

    body_text = await page.locator("body").inner_text()
    price_matches = re.findall(
        r"£\s*([0-9]{1,4}(?:,[0-9]{3})*(?:\.[0-9]{2})?)",
        body_text,
    )
    prices = [parse_price(value) for value in price_matches]
    prices = [price for price in prices if price is not None]
    return min(prices) if prices else None


async def open_product(page, model, url):
    url = clean_product_url(url)

    for attempt in range(MAX_429_RETRIES + 1):
        try:
            response = await page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=PAGE_TIMEOUT_MS,
            )
        except Exception as exc:
            print(f"    -> navigation failed: {exc}")
            return {"status": "ERROR", "price": None, "url": url}

        status = response.status if response else None
        print(f"    -> {RETAILER} HTTP: {status}")

        if status != 429:
            break
        if attempt == MAX_429_RETRIES:
            return {"status": "RATE_LIMITED", "price": None, "url": url}

        retry_after = response.headers.get("retry-after", "")
        try:
            delay = float(retry_after)
        except (TypeError, ValueError):
            delay = min(60, (2 ** attempt) * 10)
        delay += random.uniform(1, 4)
        print(f"    -> rate limited; waiting {delay:.1f}s")
        await page.wait_for_timeout(int(delay * 1000))

    if response and response.status == 404:
        return {"status": "NOT_FOUND", "price": None, "url": url}
    if response and response.status >= 400:
        return {"status": f"HTTP_{response.status}", "price": None, "url": url}

    await page.wait_for_timeout(WAIT_AFTER_LOAD_MS)
    body_text = await page.locator("body").inner_text()
    if normalize(model) not in normalize(body_text):
        print(f"    -> model mismatch: {model}")
        return {"status": "MODEL_MISMATCH", "price": None, "url": url}

    price = await extract_price(page)
    if price is None:
        return {"status": "PRICE_NOT_FOUND", "price": None, "url": url}
    return {"status": "OK", "price": price, "url": url}


async def get_currys_price(page, model, cache):
    cache_key = normalize(model)
    cached_url = cache.get(cache_key)

    if cached_url:
        print(f"    -> cached URL: {cached_url}")
        result = await open_product(page, model, cached_url)
        if result["status"] in {"OK", "RATE_LIMITED"}:
            return result
        cache.pop(cache_key, None)
        save_cache(cache)

    discovery = await asyncio.to_thread(discover_with_serpapi, model)
    if not discovery:
        return {"status": "NOT_FOUND", "price": None, "url": None}

    result = await open_product(page, model, discovery["url"])

    if (
        result["status"] == "HTTP_403"
        and discovery["price"] is not None
    ):
        print(f"    -> using exact {RETAILER} price supplied by SerpApi")
        result = {
            "status": "OK",
            "price": discovery["price"],
            "url": discovery["url"],
        }

    if result["status"] == "OK":
        cache[cache_key] = result["url"]
        save_cache(cache)
    return result


async def main():
    products = read_products()
    models = [product["model"] for product in products]
    print(f"Found {len(products)} product(s) in {INPUT_FILE}")
    print(f"SerpApi key loaded: {'YES' if SERPAPI_KEY else 'NO'}")

    if not SERPAPI_KEY:
        print("ERROR: Add SERPAPI_KEY to .env")
        return 1

    workbook, worksheet = get_or_create_workbook(models)
    cache = load_cache()

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=HEADLESS)
        context = await browser.new_context(
            locale="en-GB",
            viewport={"width": 1440, "height": 1000},
        )
        page = await context.new_page()
        page.set_default_timeout(PAGE_TIMEOUT_MS)

        for index, product in enumerate(products, start=1):
            model = product["model"]
            print("\n" + "=" * 70)
            print(f"[{index}/{len(products)}] {RETAILER}: {model}")
            print("=" * 70)

            try:
                result = await get_currys_price(page, model, cache)
            except Exception as exc:
                print(f"    -> unexpected error: {exc!r}")
                result = {"status": "ERROR", "price": None, "url": None}

            value = result["price"] if result["status"] == "OK" else result["status"]
            update_retailer_cell(
                worksheet,
                RETAILER,
                model,
                value,
                url=result.get("url"),
            )
            workbook.save(OUTPUT_FILE)
            print(f"    -> result: {value}")
            print("    -> workbook saved")

            if index < len(products):
                delay = random.uniform(
                    MIN_PRODUCT_DELAY_SECONDS,
                    MAX_PRODUCT_DELAY_SECONDS,
                )
                print(f"    -> waiting {delay:.1f}s before next product")
                await page.wait_for_timeout(int(delay * 1000))

        await context.close()
        await browser.close()

    workbook.save(OUTPUT_FILE)
    print(f"\n{RETAILER} finished. Output: {OUTPUT_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
