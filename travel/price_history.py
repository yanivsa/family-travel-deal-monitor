"""
Price history tracking and price drop / material change detection module.
Tracks historical deal snapshots in history.jsonl and calculates exact-scope price drops.
"""

import json
from pathlib import Path
from typing import Dict, List, Any

def append_to_history(history_file: Path, checked_at: str, deals: List[Dict[str, Any]]) -> None:
    """Appends a snapshot of verified top 3 deals to history.jsonl."""
    history_file.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "checked_at": checked_at,
        "deals": [
            {
                "category": d.get("category"),
                "destination": d.get("destination"),
                "total_ils": d.get("total_ils"),
                "family_value": d.get("family_value")
            }
            for d in deals
        ]
    }
    with history_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

def detect_meaningful_changes(old_payload: Dict[str, Any], new_payload: Dict[str, Any]) -> List[str]:
    """
    Detects meaningful changes between deal snapshots.
    Criteria:
    - Destination change per category
    - Price change >= ₪300 or >= 4%
    - Effective Vacation Time change >= 6 hours
    """
    old_by_cat = {d["category"]: d for d in old_payload.get("deals", []) if "category" in d}
    changes = []

    for nd in new_payload.get("deals", []):
        cat = nd.get("category")
        od = old_by_cat.get(cat)

        if not od:
            changes.append(f"NEW {cat}: {nd.get('destination')} (₪{nd.get('total_ils', 0):,.0f})")
            continue

        old_dest = od.get("destination")
        new_dest = nd.get("destination")
        if old_dest != new_dest:
            changes.append(f"{cat} changed: {old_dest} → {new_dest}")

        old_price = float(od.get("total_ils", 0))
        new_price = float(nd.get("total_ils", 0))

        if old_price > 0 and new_price > 0:
            delta = new_price - old_price
            pct = (delta / old_price) * 100

            if abs(delta) >= 300 or abs(pct) >= 4.0:
                direction = "PRICE DROP" if delta < 0 else "price increase"
                changes.append(f"{cat} {new_dest} {direction}: ₪{delta:+,.0f} ({pct:+.1f}%) [₪{old_price:,.0f} → ₪{new_price:,.0f}]")

        old_evt = float(od.get("effective_vacation_hours_num", od.get("effective_vacation_hours", 0)))
        new_evt = float(nd.get("effective_vacation_hours_num", nd.get("effective_vacation_hours", 0)))

        if abs(new_evt - old_evt) >= 6:
            changes.append(f"{cat} {new_dest}: Effective vacation time changed ({old_evt:.0f}h → {new_evt:.0f}h)")

    return changes
