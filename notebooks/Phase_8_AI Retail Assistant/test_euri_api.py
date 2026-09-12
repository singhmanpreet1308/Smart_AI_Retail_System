"""Run an Euri authentication smoke test; this does not verify web search.

From this folder or a notebook: %run test_euri_api.py
Uses EURI_API_KEY from the environment or the project-root .env file.
Requires only Python's standard library.
"""

import json
import os
from pathlib import Path
import urllib.error
import urllib.request


def load_api_key():
    key = os.environ.get("EURI_API_KEY")
    env_path = Path(__file__).resolve().parents[2] / ".env"
    if not key and env_path.exists():
        for line in env_path.read_text(encoding="utf-8-sig").splitlines():
            name, separator, value = line.partition("=")
            if separator and name.strip() == "EURI_API_KEY":
                key = value.strip().strip("\"'")
                break
    if not key:
        raise SystemExit("Set EURI_API_KEY in your environment or project-root .env.")
    return key


def main():
    key = load_api_key()

    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": "Reply with exactly OK."}],
        "max_tokens": 8,
    }
    request = urllib.request.Request(
        "https://api.euron.one/api/v1/euri/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": "Bearer " + key,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=40) as response:
            result = json.load(response)
            content = result["choices"][0]["message"]["content"]
            print(f"HTTP {response.status}: {content}".replace(key, "[REDACTED]"))
            print("Authentication succeeded. Web search has not been tested.")
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"Euri request failed: HTTP {exc.code}.") from None
    except urllib.error.URLError:
        raise SystemExit("Unable to connect to Euri. Check network access.") from None
    except (KeyError, IndexError, TypeError, ValueError):
        raise SystemExit("Euri returned an unexpected response format.") from None


if __name__ == "__main__":
    main()
