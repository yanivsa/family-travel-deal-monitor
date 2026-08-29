import json
import os
import sys
import urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from travel.guards import validate_deal_guards, is_allowed_date_pair, is_morning_return, is_destination_excluded
from travel.scoring import calculate_evt_hours, get_time_value, calculate_family_value
from travel.price_history import append_to_history, detect_meaningful_changes
from travel.adapters.providers import aggregate_provider_deals

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "travel" / "data.json"
HISTORY = ROOT / "travel" / "history.jsonl"
ALERT = ROOT / "travel" / "alert.md"
TZ = ZoneInfo("Asia/Jerusalem")
CATEGORIES = ["BEST VALUE", "BEST PRICE", "SMART UPGRADE / SURPRISE"]

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def validate(payload):
    deals = payload.get("deals", [])
    if len(deals) != 3:
        raise ValueError("provider payload must contain exactly 3 deals")
    if [d.get("category") for d in deals] != CATEGORIES:
        raise ValueError("categories/order do not match output contract")
    for d in deals:
        valid, reason = validate_deal_guards(d)
        if not valid:
            raise ValueError(f"guard validation failed: {reason}")
        if not d.get("verified", True):
            raise ValueError("unverified deal cannot replace last-known-good Top 3")
        if not isinstance(d.get("total_ils"), (int, float)) or d["total_ils"] <= 0:
            raise ValueError("invalid total_ils")
        if not d.get("flight_url") or not d.get("hotel_url"):
            raise ValueError("reproducible flight_url and hotel_url are required")
    return payload

def rank_top_three_deals(candidate_deals: list) -> list:
    """Ranks candidates into BEST VALUE, BEST PRICE, SMART UPGRADE / SURPRISE."""
    if len(candidate_deals) < 3:
        raise ValueError("Insufficient verified candidate deals to build Top 3")

    # Sort by price
    by_price = sorted(candidate_deals, key=lambda x: x.get("total_ils", float("inf")))
    best_price_deal = dict(by_price[0])

    # Sort by family value score
    by_value = sorted(candidate_deals, key=lambda x: x.get("family_value", 0), reverse=True)
    best_value_deal = dict(by_value[0])

    # If best_value_deal is the same as best_price_deal, pick the next highest value
    if best_value_deal == best_price_deal and len(by_value) > 1:
        best_value_deal = dict(by_value[1])

    # Select upgrade / surprise candidate
    remaining = [d for d in candidate_deals if d != best_price_deal and d != best_value_deal]
    if not remaining:
        remaining = [d for d in candidate_deals if d != best_price_deal]
    if not remaining:
        remaining = candidate_deals

    by_upgrade = sorted(remaining, key=lambda x: (x.get("stars", 0), x.get("guest_score", 0), x.get("total_ils", 0)), reverse=True)
    upgrade_deal = dict(by_upgrade[0])

    # Assign ranks and categories
    best_value_deal["rank"] = 1
    best_value_deal["category"] = "BEST VALUE"

    best_price_deal["rank"] = 2
    best_price_deal["category"] = "BEST PRICE"

    upgrade_deal["rank"] = 3
    upgrade_deal["category"] = "SMART UPGRADE / SURPRISE"

    return [best_value_deal, best_price_deal, upgrade_deal]

def main():
    current = load(DATA)
    verified_candidates = []

    try:
        verified_candidates = aggregate_provider_deals()
    except Exception as e:
        print(f"Provider adapters encountered error: {e}; preserving last-known-good data.", file=sys.stderr)

    if not verified_candidates:
        print("No new verified live provider deals retrieved; preserving last-known-good data.")
        ALERT.unlink(missing_ok=True)
        return 0

    try:
        ranked_deals = rank_top_three_deals(verified_candidates)
        incoming = dict(current)
        incoming["deals"] = ranked_deals
        incoming["generated_at"] = datetime.now(TZ).isoformat()
        if "automation" not in incoming:
            incoming["automation"] = {}
        incoming["automation"]["last_attempt_at"] = incoming["generated_at"]
        incoming["automation"]["last_verified_live_refresh"] = incoming["generated_at"]

        validated_payload = validate(incoming)
    except Exception as e:
        print(f"Live candidates failed ranking/validation: {e}; preserving last-known-good data.", file=sys.stderr)
        ALERT.unlink(missing_ok=True)
        return 0

    checked_at_str = datetime.now(TZ).strftime("%Y-%m-%d %H:%M Asia/Jerusalem")
    validated_payload["checked_at"] = checked_at_str

    changes = detect_meaningful_changes(current, validated_payload)

    DATA.write_text(json.dumps(validated_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    append_to_history(HISTORY, checked_at_str, validated_payload["deals"])

    if changes:
        body = "# Travel deal monitor — meaningful change\n\n" + "\n".join(f"- {x}" for x in changes) + "\n\nDashboard: https://yanivsa.github.io/family-travel-deal-monitor/\n"
        ALERT.write_text(body, encoding="utf-8")
    else:
        ALERT.unlink(missing_ok=True)

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
