#!/usr/bin/env python3
"""Convert the sibling hyperliquid-bruno OpenCollection files to native Bruno."""

from __future__ import annotations

import argparse
import json
import re
import textwrap
from pathlib import Path


FOLDERS = (
    ("info", "Info", 1),
    ("perpetuals", "Perpetuals", 2),
    ("spot", "Spot", 3),
    ("exchange", "Exchange", 4),
    ("websocket-payloads", "Websocket Payloads", 5),
)

# The source collection intentionally uses placeholders. Prefer stable, public
# examples where a placeholder makes an otherwise read-only request fail.
BODY_OVERRIDES = {
    "perpDexLimits": {"type": "perpDexLimits", "dex": "xyz"},
    "tokenDetails": {
        "type": "tokenDetails",
        "tokenId": "0x6d1e7cde53ba9467b783cb7c530ce054",
    },
}


def indent(text: str, spaces: int = 2) -> str:
    prefix = " " * spaces
    return "\n".join(f"{prefix}{line}" if line else "" for line in text.splitlines())


def request_filename(source: Path) -> str:
    return re.sub(r"^\d+-", "", source.stem) + ".bru"


def parse_docs(text: str, source: Path) -> str:
    block = re.search(r"^docs: \|-\n(.*)\Z", text, flags=re.MULTILINE | re.DOTALL)
    if block:
        return textwrap.dedent(block.group(1)).strip()
    scalar = re.search(r"^docs: (.*?)\s*\Z", text, flags=re.MULTILINE | re.DOTALL)
    if scalar:
        return scalar.group(1).strip()
    raise ValueError(f"Could not parse docs in {source}")


def parse_request(source: Path) -> dict:
    text = source.read_text(encoding="utf-8")

    def match(pattern: str) -> str:
        found = re.search(pattern, text, flags=re.MULTILINE | re.DOTALL)
        if not found:
            raise ValueError(f"Could not parse {source}: {pattern}")
        return found.group(1).strip()

    body_block = match(r"^    data: \|-\n(.*?)^  auth:")
    return {
        "info": {
            "name": match(r"^  name: (.*?)$"),
            "type": match(r"^  type: (.*?)$"),
            "seq": int(match(r"^  seq: (\d+)$")),
        },
        "http": {
            "method": match(r"^  method: (.*?)$"),
            "url": match(r"^  url: (.*?)$"),
            "body": {"data": textwrap.dedent(body_block)},
        },
        "docs": parse_docs(text, source),
    }


def parse_folder_docs(source: Path) -> str:
    text = source.read_text(encoding="utf-8")
    return parse_docs(text, source)


def folder_file(name: str, seq: int, docs: str) -> str:
    return f"""meta {{
  name: {name}
  seq: {seq}
}}

docs {{
{indent(docs)}
}}
"""


def request_file(data: dict, folder_key: str) -> str:
    info = data["info"]
    http = data["http"]
    if info.get("type") != "http" or http.get("method") != "POST":
        raise ValueError(f"Unsupported request shape: {info.get('name')}")

    raw_url = http["url"]
    if raw_url.startswith("https://api.hyperliquid.xyz"):
        url = raw_url.replace("https://api.hyperliquid.xyz", "{{baseUrl}}", 1)
    else:
        raise ValueError(f"Unexpected Hyperliquid URL: {raw_url}")

    parsed_body = json.loads(http["body"]["data"])
    parsed_body = BODY_OVERRIDES.get(parsed_body.get("type"), parsed_body)
    body = json.dumps(parsed_body, indent=2)
    path = raw_url.removeprefix("https://api.hyperliquid.xyz")
    access = "signed action template" if folder_key == "exchange" else "public Info request"
    docs = data.get("docs", "").strip()
    reference = (
        "https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint"
        if folder_key == "exchange"
        else "https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint"
    )

    return f"""meta {{
  name: {info['name']}
  type: http
  seq: {info['seq']}
}}

post {{
  url: {url}
  body: json
  auth: inherit
}}

body:json {{
{indent(body)}
}}

settings {{
  encodeUrl: true
  timeout: 0
}}

docs {{
  {info['name']}

  POST {path} ({access})

{indent(docs)}

  Reference: {reference}
}}
"""


def write_collection(source: Path, target: Path) -> None:
    target.mkdir(parents=True, exist_ok=True)
    (target / "environments").mkdir(exist_ok=True)

    (target / "bruno.json").write_text(
        json.dumps(
            {
                "version": "1",
                "name": "hyperliquid",
                "type": "collection",
                "ignore": ["node_modules", ".git"],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    (target / "collection.bru").write_text(
        """auth {
  mode: none
}

headers {
  Accept: application/json
  Content-Type: application/json
}

docs {
  # Hyperliquid API

  Native Bruno requests for Hyperliquid's Info and Exchange endpoints.
  Info requests are public. Exchange requests contain inert placeholder
  signatures and must be replaced with correctly signed actions before use.

  Base URLs:
  - production: https://api.hyperliquid.xyz
  - testnet: https://api.hyperliquid-testnet.xyz

  References:
  - https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint
  - https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/exchange-endpoint
}
""",
        encoding="utf-8",
    )

    environments = {
        "production": "https://api.hyperliquid.xyz",
        "testnet": "https://api.hyperliquid-testnet.xyz",
    }
    for name, base_url in environments.items():
        (target / "environments" / f"{name}.bru").write_text(
            f"vars {{\n  baseUrl: {base_url}\n}}\n", encoding="utf-8"
        )

    for source_name, target_name, seq in FOLDERS:
        source_folder = source / source_name
        target_folder = target / target_name
        target_folder.mkdir(exist_ok=True)
        (target_folder / "folder.bru").write_text(
            folder_file(target_name, seq, parse_folder_docs(source_folder / "folder.yml")),
            encoding="utf-8",
        )

        for source_file in sorted(source_folder.glob("*.yml")):
            if source_file.name == "folder.yml":
                continue
            request_data = parse_request(source_file)
            (target_folder / request_filename(source_file)).write_text(
                request_file(request_data, source_name), encoding="utf-8"
            )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path, help="Path to the hyperliquid-bruno source collection")
    parser.add_argument("target", type=Path, help="Destination directory for the native Bruno collection")
    args = parser.parse_args()
    write_collection(args.source.resolve(), args.target.resolve())


if __name__ == "__main__":
    main()
