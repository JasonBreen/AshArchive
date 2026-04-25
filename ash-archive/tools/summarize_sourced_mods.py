#!/usr/bin/env python3
from __future__ import annotations

from lib.manifest import load_yaml
from lib.paths import ROOT


def main() -> int:
    data = load_yaml(ROOT / "shared" / "sourced-mods.yaml")
    buckets = data.get("buckets", [])
    for bucket in buckets:
        print(f"\n[{bucket.get('name', 'unknown')}]")
        print("name | source")
        print("---- | ------")
        for cand in bucket.get("candidates", []):
            print(f"{cand.get('name', '')} | {cand.get('source', '')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
