"""Five-product Euri pilot. Search tools are experimental, not assumed supported.

Candidate model output is kept separately from the empty verified-spec fields.
No specification is promoted without independent source review.
"""
import json
import os
from datetime import datetime, timezone
from pathlib import Path
import urllib.error
import urllib.request

from test_euri_api import load_api_key
from product_specs_prompt import build_prompt

PRODUCTS = [
    ("Samsung", "DV90DB8845"),
    ("Samsung", "MC28H5013AS/EU"),
    ("Samsung", "NV68A1170BS/EU"),
    ("LG", "32LQ63006LA.AEK"),
    ("LG", "43LQ60006LA.LG"),
]
FIELDS = "official_model product_name category width_mm height_mm depth_mm screen_size_in capacity_value capacity_unit power_w energy_rating warranty primary_source_url source_type confidence data_completeness".split()


def parse_candidate(response):
    text = response["choices"][0]["message"].get("content") or ""
    if text.strip().startswith("```"):
        text = "\n".join(text.strip().splitlines()[1:-1])
    candidate = json.loads(text)
    if not isinstance(candidate, dict):
        raise ValueError("Expected a JSON object")
    return candidate


def get_product_specs_with_llm(manufacturer, model):
    key = load_api_key()
    row = dict.fromkeys(FIELDS)
    row.update(manufacturer=manufacturer, requested_model=model,
               match_status="UNVERIFIED", key_features=[], additional_source_urls=[],
               search_status="UNCONFIRMED", candidate_specs=None, error=None,
               tested_at_utc=datetime.now(timezone.utc).isoformat())
    payload = {
        "model": os.environ.get("EURI_MODEL", "gpt-5.6"),
        "messages": [{"role": "user", "content": build_prompt(manufacturer, model)}],
        "tools": [{"type": "web_search"}],
        "max_tokens": 2500,
    }
    request = urllib.request.Request(
        "https://api.euron.one/api/v1/euri/chat/completions",
        data=json.dumps(payload).encode(),
        headers={"Authorization": "Bearer " + key,
                 "Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            # Redact any accidental echo before persisting provider output.
            raw = response.read().decode().replace(key, "[REDACTED]")
            result = json.loads(raw)
            row["http_status"] = response.status
        row["api_response"] = result
        row["api_model"] = result.get("model")
        message = result.get("choices", [{}])[0].get("message", {})
        evidence = {k: message[k] for k in ("annotations", "tool_calls") if message.get(k)}
        for k in ("citations", "sources", "output"):
            if result.get(k):
                evidence[k] = result[k]
        row["search_metadata"] = evidence
        row["search_status"] = "METADATA_REQUIRES_REVIEW" if evidence else "NO_SEARCH_EVIDENCE"
        try:
            row["candidate_specs"] = parse_candidate(result)
        except (ValueError, KeyError, IndexError, TypeError):
            row["error"] = "JSON_OR_RESPONSE_FORMAT_ERROR"
    except urllib.error.HTTPError as exc:
        row.update(http_status=exc.code, error=f"HTTP_{exc.code}", search_status="REQUEST_REJECTED")
    except (urllib.error.URLError, TimeoutError):
        row["error"] = "NETWORK_ERROR"
    except (ValueError, KeyError, IndexError, TypeError):
        row["error"] = "JSON_OR_RESPONSE_FORMAT_ERROR"
    return row


def run_pilot():
    rows = []
    for manufacturer, model in PRODUCTS:
        print(f"Retrieving: {manufacturer} {model}", flush=True)
        row = get_product_specs_with_llm(manufacturer, model)
        rows.append(row)
        print(f"  {row['search_status']} | {row['error'] or 'response received'}", flush=True)
    path = Path(__file__).with_name("euri_pilot_results.json")
    path.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    print("Saved diagnostic results:", path)
    print("Verified fields remain empty pending source review; candidate_specs is unverified.")
    return rows


if __name__ == "__main__":
    llm_results = run_pilot()
