#!/usr/bin/env python3

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
    get_or_create_workbook,
    update_retailer_cell,
    OUTPUT_FILE,
    INPUT_FILE,
)


# ============================================================
# LOAD .ENV
# ============================================================

load_dotenv()


# ============================================================
# CONFIG
# ============================================================

RETAILER = "Harvey Norman"

HARVEY_DOMAIN = "harveynorman.co.uk"

CACHE_FILE = "harvey_urls.json"

HEADLESS = False

PAGE_TIMEOUT = 60000

WAIT_AFTER_LOAD_MS = 3000

MAX_429_RETRIES = 3

MIN_PRODUCT_DELAY_SECONDS = 8

MAX_PRODUCT_DELAY_SECONDS = 15


# ============================================================
# SERPAPI
# ============================================================

SERPAPI_KEY = os.getenv(
    "SERPAPI_KEY",
    ""
).strip()

SERPAPI_ENDPOINT = (
    "https://serpapi.com/search.json"
)


# ============================================================
# READ SOA.XLSX
# ============================================================

def read_products(
    input_path=INPUT_FILE
):
    """
    Expected structure:

        Column A = Model
        Column B = Description
    """

    workbook = openpyxl.load_workbook(
        input_path,
        data_only=True,
    )

    worksheet = workbook.active

    products = []

    for row in worksheet.iter_rows(
        min_row=2,
        values_only=True,
    ):

        if not row:
            continue

        model = ""

        description = ""

        if (
            len(row) >= 1
            and row[0] is not None
        ):
            model = str(
                row[0]
            ).strip()

        if (
            len(row) >= 2
            and row[1] is not None
        ):
            description = str(
                row[1]
            ).strip()

        if not model:
            continue

        products.append(
            {
                "model": model,
                "description": description,
            }
        )

    workbook.close()

    return products


# ============================================================
# NORMALISATION
# ============================================================

def normalize(text):
    """
    ES-601 UK -> ES601UK
    """

    return re.sub(
        r"[^A-Z0-9]",
        "",
        str(text or "").upper(),
    )


def clean_product_url(url):
    """Remove search-engine tracking parameters from product URLs."""

    parts = urlsplit(url)

    return urlunsplit(
        (
            parts.scheme,
            parts.netloc,
            parts.path,
            "",
            "",
        )
    )


def description_words(
    description
):
    """
    Extract useful words for fuzzy matching.
    """

    words = re.findall(
        r"[a-z0-9]+",
        str(description or "").lower(),
    )

    ignore = {
        "the",
        "and",
        "for",
        "with",
        "from",
        "of",
        "a",
        "an",
        "uk",
    }

    return [
        word
        for word in words
        if (
            word not in ignore
            and len(word) >= 3
        )
    ]


# ============================================================
# CACHE
# ============================================================

def load_cache():

    path = Path(
        CACHE_FILE
    )

    if not path.exists():
        return {}

    try:

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(
                file
            )

        if isinstance(
            data,
            dict
        ):
            return data

    except Exception as exc:

        print(
            f"    -> cache warning: "
            f"{exc}"
        )

    return {}


def save_cache(
    cache
):

    with open(
        CACHE_FILE,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            cache,
            file,
            indent=2,
            ensure_ascii=False,
        )


# ============================================================
# PRICE HELPERS
# ============================================================

def clean_price(
    text
):

    if not text:
        return None

    match = re.search(
        r"(?:£|GBP\s*)\s*"
        r"([\d,]+(?:\.\d{1,2})?)",
        str(text),
        re.IGNORECASE,
    )

    if not match:
        return None

    try:

        return float(
            match.group(1)
            .replace(",", "")
        )

    except ValueError:

        return None


# ============================================================
# JSON-LD PRICE
# ============================================================

def find_price_in_json(
    data
):

    if isinstance(
        data,
        list
    ):

        for item in data:

            price = (
                find_price_in_json(
                    item
                )
            )

            if price is not None:
                return price

        return None

    if not isinstance(
        data,
        dict
    ):
        return None

    item_type = data.get(
        "@type"
    )

    if isinstance(
        item_type,
        list
    ):

        types = [
            str(value).lower()
            for value in item_type
        ]

    else:

        types = [
            str(item_type).lower()
        ]

    if (
        "offer" in types
        or "aggregateoffer" in types
    ):

        possible_prices = [
            data.get("price"),
            data.get("lowPrice"),
            data.get("highPrice"),
        ]

        for value in possible_prices:

            if value is None:
                continue

            try:

                return float(
                    str(value)
                    .replace("£", "")
                    .replace(",", "")
                    .strip()
                )

            except ValueError:

                continue

    if "offers" in data:

        price = find_price_in_json(
            data["offers"]
        )

        if price is not None:
            return price

    for value in data.values():

        if isinstance(
            value,
            (dict, list)
        ):

            price = find_price_in_json(
                value
            )

            if price is not None:
                return price

    return None


async def extract_price_json_ld(
    page
):

    scripts = page.locator(
        'script[type="application/ld+json"]'
    )

    try:

        count = await scripts.count()

    except Exception:

        return None

    print(
        f"    -> JSON-LD blocks: "
        f"{count}"
    )

    for index in range(
        count
    ):

        try:

            raw = (
                await scripts
                .nth(index)
                .text_content()
            )

            if not raw:
                continue

            raw = raw.strip()

            if not raw:
                continue

            data = json.loads(
                raw
            )

            price = find_price_in_json(
                data
            )

            if price is not None:

                print(
                    f"    -> JSON-LD price: "
                    f"£{price:.2f}"
                )

                return price

        except Exception:

            continue

    return None


# ============================================================
# META PRICE
# ============================================================

async def extract_price_meta(
    page
):

    selectors = [
        'meta[property="product:price:amount"]',
        'meta[property="og:price:amount"]',
        'meta[itemprop="price"]',
        'meta[name="price"]',
    ]

    for selector in selectors:

        locator = page.locator(
            selector
        )

        try:

            count = await locator.count()

        except Exception:

            continue

        for index in range(
            count
        ):

            try:

                content = (
                    await locator
                    .nth(index)
                    .get_attribute(
                        "content"
                    )
                )

                if not content:
                    continue

                price = clean_price(
                    content
                )

                if price is None:

                    try:

                        price = float(
                            content
                            .replace(",", "")
                            .strip()
                        )

                    except ValueError:

                        price = None

                if price is not None:

                    print(
                        f"    -> meta price: "
                        f"£{price:.2f}"
                    )

                    return price

            except Exception:

                continue

    return None


# ============================================================
# VISIBLE PRICE ELEMENTS
# ============================================================

async def extract_price_elements(
    page
):

    selectors = [
        ".price-item--sale",
        ".price-item--regular",
        ".price-item",
        ".price__regular",
        ".price__sale",
        ".product__price",
        ".product-price",
        "[data-product-price]",
        "[data-price]",
        '[itemprop="price"]',
    ]

    for selector in selectors:

        locator = page.locator(
            selector
        )

        try:

            count = await locator.count()

        except Exception:

            continue

        for index in range(
            min(count, 20)
        ):

            try:

                text = (
                    await locator
                    .nth(index)
                    .inner_text()
                )

                price = clean_price(
                    text
                )

                if price is not None:

                    print(
                        f"    -> element price: "
                        f"£{price:.2f}"
                    )

                    return price

            except Exception:

                continue

    return None


# ============================================================
# PAGE TEXT PRICE
# ============================================================

async def extract_price_page_text(
    page
):

    try:

        text = (
            await page
            .locator("body")
            .inner_text()
        )

    except Exception:

        return None

    candidates = []

    for line in text.splitlines():

        lower = line.lower()

        if any(
            phrase in lower
            for phrase in [
                "per month",
                "monthly",
                "finance",
                "apr",
                "deposit",
            ]
        ):
            continue

        matches = re.findall(
            r"£\s*"
            r"([\d,]+(?:\.\d{1,2})?)",
            line,
        )

        for match in matches:

            try:

                price = float(
                    match.replace(
                        ",",
                        ""
                    )
                )

                if price > 0:

                    candidates.append(
                        price
                    )

            except ValueError:

                continue

    if not candidates:
        return None

    print(
        f"    -> visible price candidates: "
        f"{candidates[:10]}"
    )

    return candidates[0]


# ============================================================
# COMPLETE PRICE EXTRACTION
# ============================================================

async def extract_product_price(
    page
):

    print(
        "    -> trying JSON-LD..."
    )

    price = (
        await extract_price_json_ld(
            page
        )
    )

    if price is not None:
        return price

    print(
        "    -> trying meta tags..."
    )

    price = (
        await extract_price_meta(
            page
        )
    )

    if price is not None:
        return price

    print(
        "    -> trying visible price elements..."
    )

    price = (
        await extract_price_elements(
            page
        )
    )

    if price is not None:
        return price

    print(
        "    -> trying page text..."
    )

    return (
        await extract_price_page_text(
            page
        )
    )


# ============================================================
# MODEL VERIFICATION
# ============================================================

async def page_contains_model(
    page,
    model
):

    target = normalize(
        model
    )

    try:

        title = await page.title()

    except Exception:

        title = ""

    try:

        body = (
            await page
            .locator("body")
            .inner_text()
        )

    except Exception:

        body = ""

    combined = (
        title
        + " "
        + body[:20000]
        + " "
        + page.url
    )

    normalized = normalize(
        combined
    )

    if target in normalized:
        return True

    # --------------------------------------------------------
    # Prefix fallback
    # Useful for colour suffixes such as:
    # JBLLIVE770NCBLK
    # --------------------------------------------------------

    if len(target) >= 8:

        prefix = target[:8]

        if prefix in normalized:
            return True

    return False


# ============================================================
# SERPAPI RESULT SCORING
# ============================================================

def score_search_result(
    result,
    model,
    description,
):

    link = str(
        result.get(
            "link",
            ""
        )
    )

    title = str(
        result.get(
            "title",
            ""
        )
    )

    snippet = str(
        result.get(
            "snippet",
            ""
        )
    )

    if not link:
        return -1000

    if (
        "harveynorman.co.uk/products/"
        not in link.lower()
    ):
        return -1000

    score = 0

    target_model = normalize(
        model
    )

    combined = normalize(
        link
        + " "
        + title
        + " "
        + snippet
    )

    normalized_link = normalize(link)
    normalized_title = normalize(title)

    # Do not let description-word matches select an unrelated product.
    if not target_model or target_model not in combined:
        return -1000

    # Exact model
    if target_model in normalized_link:
        score += 200

    if target_model in normalized_title:
        score += 150

    if target_model in combined:
        score += 100

    # Model family / prefix
    if len(target_model) >= 8:

        prefix = target_model[:8]

        if prefix in combined:
            score += 30

    # Description similarity
    searchable = (
        link
        + " "
        + title
        + " "
        + snippet
    ).lower()

    for word in description_words(
        description
    ):

        if word in searchable:
            score += 3

    return score


# ============================================================
# SERPAPI DISCOVERY
# ============================================================

def discover_with_serpapi(
    model,
    description
):

    if not SERPAPI_KEY:

        print(
            "    -> ERROR: "
            "SERPAPI_KEY is not loaded"
        )

        return None

    # --------------------------------------------------------
    # Keep query simple.
    # Model number is strongest identifier.
    # --------------------------------------------------------

    query = (
        f'site:harveynorman.co.uk/products '
        f'"{model}"'
    )

    print()
    print(
        "    -> SERPAPI SEARCH"
    )

    print(
        f"       Query: {query}"
    )

    print(
        f"       API key loaded: "
        f"{'YES' if SERPAPI_KEY else 'NO'}"
    )

    params = {
        "engine": "google",
        "q": query,
        "google_domain": "google.co.uk",
        "gl": "uk",
        "hl": "en",
        "num": 10,
        "api_key": SERPAPI_KEY,
    }

    try:

        response = requests.get(
            SERPAPI_ENDPOINT,
            params=params,
            timeout=30,
        )

        print(
            f"    -> SerpApi HTTP status: "
            f"{response.status_code}"
        )

        response.raise_for_status()

        data = response.json()

    except requests.RequestException as exc:

        print(
            f"    -> SerpApi request failed:"
        )

        print(
            f"       {exc}"
        )

        return None

    except ValueError as exc:

        print(
            f"    -> invalid SerpApi JSON:"
        )

        print(
            f"       {exc}"
        )

        return None

    # --------------------------------------------------------
    # API-level error
    # --------------------------------------------------------

    if "error" in data:

        print(
            "    -> SERPAPI ERROR:"
        )

        print(
            f"       {data['error']}"
        )

        return None

    organic_results = data.get(
        "organic_results",
        []
    )

    print(
        f"    -> organic results found: "
        f"{len(organic_results)}"
    )

    # --------------------------------------------------------
    # Print all returned results
    # --------------------------------------------------------

    for index, result in enumerate(
        organic_results,
        start=1
    ):

        print()
        print(
            f"       RESULT {index}"
        )

        print(
            f"       Title: "
            f"{result.get('title', '')}"
        )

        print(
            f"       Link: "
            f"{result.get('link', '')}"
        )

    if not organic_results:

        return None

    # --------------------------------------------------------
    # Score results
    # --------------------------------------------------------

    scored = []

    for result in organic_results:

        score = score_search_result(
            result,
            model,
            description,
        )

        if score > 0:

            scored.append(
                (
                    score,
                    result,
                )
            )

    if not scored:

        print()
        print(
            "    -> no suitable "
            "Harvey Norman product result"
        )

        return None

    scored.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    best_score, best_result = (
        scored[0]
    )

    best_url = (
        best_result.get(
            "link"
        )
    )

    print()
    print(
        f"    -> best result score: "
        f"{best_score}"
    )

    print(
        f"    -> discovered URL:"
    )

    print(
        f"       {best_url}"
    )

    return best_url


# ============================================================
# OPEN AND VERIFY PRODUCT
# ============================================================

async def try_product_url(
    page,
    model,
    url
):

    if not url:
        return None

    url = clean_product_url(url)

    print()
    print(
        "    -> opening product:"
    )

    print(
        f"       {url}"
    )

    response = None

    for attempt in range(MAX_429_RETRIES + 1):

        try:

            response = await page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=PAGE_TIMEOUT,
            )

        except Exception as exc:

            print(
                f"    -> navigation failed:"
            )

            print(
                f"       {exc}"
            )

            return None

        status = response.status if response else None

        print(
            f"    -> product HTTP: "
            f"{status}"
        )

        if status != 429:
            break

        if attempt == MAX_429_RETRIES:
            return {
                "status": "RATE_LIMITED",
                "price": None,
                "url": url,
            }

        retry_after = response.headers.get(
            "retry-after",
            "",
        )

        try:
            delay = float(retry_after)
        except (TypeError, ValueError):
            delay = min(60, (2 ** attempt) * 10)

        delay += random.uniform(1, 4)

        print(
            f"    -> rate limited; waiting "
            f"{delay:.1f} seconds"
        )

        await page.wait_for_timeout(
            int(delay * 1000)
        )

    if response and response.status == 404:
        return None

    await page.wait_for_timeout(
        WAIT_AFTER_LOAD_MS
    )

    model_matches = (
        await page_contains_model(
            page,
            model
        )
    )

    if not model_matches:

        print(
            f"    -> MODEL MISMATCH: "
            f"{model}"
        )

        return None

    print(
        f"    -> model verified: "
        f"{model}"
    )

    price = (
        await extract_product_price(
            page
        )
    )

    if price is None:

        return {
            "status": "PRICE_NOT_FOUND",
            "price": None,
            "url": url,
        }

    return {
        "status": "OK",
        "price": price,
        "url": url,
    }


# ============================================================
# COMPLETE HARVEY LOOKUP
# ============================================================

async def get_harvey_price(
    page,
    model,
    description,
    cache,
):

    cache_key = normalize(
        model
    )

    # ========================================================
    # STAGE 1: CACHE
    # ========================================================

    cached_url = cache.get(
        cache_key
    )

    if cached_url:

        print(
            "    STAGE 1: cached URL"
        )

        print(
            f"       {cached_url}"
        )

        result = await try_product_url(
            page,
            model,
            cached_url,
        )

        if (
            result is not None
            and result["status"] == "OK"
        ):

            return result

        if (
            result is not None
            and result["status"] == "RATE_LIMITED"
        ):

            # A temporary rate limit does not invalidate the cached URL.
            return result

        print(
            "    -> cached URL failed; "
            "removing cache entry"
        )

        cache.pop(
            cache_key,
            None,
        )

        save_cache(
            cache
        )

    # ========================================================
    # STAGE 2: SERPAPI
    # ========================================================

    print(
        "    STAGE 2: SerpApi discovery"
    )

    discovered_url = (
        discover_with_serpapi(
            model,
            description,
        )
    )

    if not discovered_url:

        return {
            "status": "NOT_FOUND",
            "price": None,
            "url": None,
        }

    result = await try_product_url(
        page,
        model,
        discovered_url,
    )

    if result is None:

        return {
            "status": "NOT_FOUND",
            "price": None,
            "url": discovered_url,
        }

    # --------------------------------------------------------
    # Save successful URL
    # --------------------------------------------------------

    if result["status"] == "OK":

        cache[
            cache_key
        ] = result["url"]

        save_cache(
            cache
        )

        print(
            "    -> URL saved to "
            "harvey_urls.json"
        )

    return result


# ============================================================
# MAIN
# ============================================================

async def main():

    products = read_products()

    print()
    print(
        f"Found {len(products)} "
        f"product(s) in {INPUT_FILE}"
    )

    print(
        f"SerpApi key loaded: "
        f"{'YES' if SERPAPI_KEY else 'NO'}"
    )

    if not SERPAPI_KEY:

        print()
        print(
            "ERROR:"
        )

        print(
            "SERPAPI_KEY is missing."
        )

        print(
            "Check your .env file."
        )

        return

    models = [
        product[
            "model"
        ]
        for product in products
    ]

    workbook, worksheet = (
        get_or_create_workbook(
            models
        )
    )

    cache = load_cache()

    async with async_playwright() as playwright:

        browser = (
            await playwright
            .chromium
            .launch(
                headless=HEADLESS
            )
        )

        context = (
            await browser.new_context(
                locale="en-GB",
                viewport={
                    "width": 1440,
                    "height": 1000,
                },
            )
        )

        page = (
            await context.new_page()
        )

        page.set_default_timeout(
            PAGE_TIMEOUT
        )

        for index, product in enumerate(
            products,
            start=1,
        ):

            model = (
                product["model"]
            )

            description = (
                product["description"]
            )

            print()
            print(
                "=" * 70
            )

            print(
                f"[{index}/{len(products)}] "
                f"{RETAILER}: {model}"
            )

            print(
                "=" * 70
            )

            print(
                f"    Description: "
                f"{description}"
            )

            try:

                result = (
                    await get_harvey_price(
                        page,
                        model,
                        description,
                        cache,
                    )
                )

                status = (
                    result[
                        "status"
                    ]
                )

                if status == "OK":

                    price = (
                        result[
                            "price"
                        ]
                    )

                    print()
                    print(
                        f"    PRICE FOUND: "
                        f"£{price:.2f}"
                    )

                    update_retailer_cell(
                        worksheet,
                        RETAILER,
                        model,
                        price,
                        url=result[
                            "url"
                        ],
                    )

                else:

                    print()
                    print(
                        f"    RESULT: "
                        f"{status}"
                    )

                    update_retailer_cell(
                        worksheet,
                        RETAILER,
                        model,
                        status,
                        url=result.get(
                            "url"
                        ),
                    )

            except Exception as exc:

                print()
                print(
                    "    UNEXPECTED ERROR:"
                )

                print(
                    f"    {repr(exc)}"
                )

                update_retailer_cell(
                    worksheet,
                    RETAILER,
                    model,
                    "ERROR",
                )

            workbook.save(
                OUTPUT_FILE
            )

            print(
                "    -> workbook saved"
            )

            if index < len(products):

                delay = random.uniform(
                    MIN_PRODUCT_DELAY_SECONDS,
                    MAX_PRODUCT_DELAY_SECONDS,
                )

                print(
                    f"    -> waiting {delay:.1f}s "
                    "before next product"
                )

                await page.wait_for_timeout(
                    int(delay * 1000)
                )

        await context.close()

        await browser.close()

    workbook.save(
        OUTPUT_FILE
    )

    print()
    print(
        "=" * 70
    )

    print(
        "HARVEY NORMAN FINISHED"
    )

    print(
        "=" * 70
    )

    print(
        f"Output: {OUTPUT_FILE}"
    )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    asyncio.run(
        main()
    )
