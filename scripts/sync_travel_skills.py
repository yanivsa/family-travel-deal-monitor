#!/usr/bin/env python3
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "travel" / "skills.json"
DEST_ROOT = ROOT / ".agents" / "skills"


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    DEST_ROOT.mkdir(parents=True, exist_ok=True)
    for skill in manifest["skills"]:
        name = skill["name"]
        url = skill["source"]
        req = urllib.request.Request(url, headers={"User-Agent": "family-travel-deal-monitor-skill-sync/1.0"})
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read().decode("utf-8")
        if not data.strip():
            raise RuntimeError(f"empty skill payload: {name}")
        target_dir = DEST_ROOT / name
        target_dir.mkdir(parents=True, exist_ok=True)
        (target_dir / "SKILL.md").write_text(data, encoding="utf-8")
        print(f"synced {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
