import json
import statistics
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
CONFIG = ROOT / "travel" / "config.json"
WHITELIST = ROOT / "travel" / "destination_whitelist.json"
FEED = ROOT / "travel" / "provider-feed.json"
DATA = ROOT / "travel" / "data.json"
HISTORY = ROOT / "travel" / "history.jsonl"
ALERT = ROOT / "travel" / "alert.md"
TZ = ZoneInfo("Asia/Jerusalem")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def parse_iso(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return dt if dt.tzinfo else dt.replace(tzinfo=TZ)


def normalize_text(value):
    return " ".join(str(value or "").strip().lower().split())


def component_keys(candidate):
    profile = candidate["destination_profile_id"]
    dep = candidate["departure_date"]
    ret = candidate["return_date"]
    hotel = normalize_text(candidate.get("hotel"))
    return {
        "flight": f"flight|{profile}|{dep}|{ret}|direct",
        "hotel": f"hotel|{hotel}|{dep}|{ret}",
        "vacation": f"vacation|{profile}|{dep}|{ret}",
    }


def candidate_observed_at(candidate):
    value = candidate.get("verified_at")
    if not value:
        raise ValueError("candidate is missing verified_at")
    return parse_iso(value)


def observation_id(candidate, key, component):
    return f"{candidate['verified_at']}|{key}|{component}"


def validate_feed(feed, config, whitelist):
    if len(whitelist) != 64:
        raise ValueError(f"destination whitelist must contain exactly 64 profiles, found {len(whitelist)}")

    feed_verified_at = feed.get("verified_at")
    if not feed_verified_at:
        raise ValueError("provider feed is missing verified_at")
    feed_time = parse_iso(feed_verified_at)
    max_age = timedelta(minutes=float(config.get("max_candidate_age_minutes", 90)))
    future_tolerance = timedelta(minutes=5)

    by_id = {item["id"]: item for item in whitelist}
    allowed_returns = set(config["return_dates"])
    expected_party = config["party"]

    feed_cfg = feed.get("config", {})
    if feed_cfg.get("origin") != config["origin"]:
        raise ValueError("feed origin does not match config")
    if feed_cfg.get("departure_date") != config["departure_date"]:
        raise ValueError("feed departure date does not match config")
    if set(feed_cfg.get("return_dates", [])) != allowed_returns:
        raise ValueError("feed return dates do not match config")
    if feed_cfg.get("direct_only") is not True:
        raise ValueError("feed must be direct-only")
    if feed_cfg.get("party") != expected_party:
        raise ValueError("feed party does not match config")

    known_gateways = {item["gateway_iata"] for item in whitelist}
    coverage = feed.get("scan_coverage", {})
    if coverage.get("whitelist_profiles") != len(whitelist):
        raise ValueError("feed whitelist profile count does not match repository whitelist")
    if coverage.get("unique_gateways_total") != len(known_gateways):
        raise ValueError("feed unique gateway count does not match repository whitelist")
    checked = set(coverage.get("gateways_live_checked_this_run", []))
    if not checked.issubset(known_gateways):
        raise ValueError("feed claims an unknown gateway in scan coverage")

    valid = []
    for candidate in feed.get("candidates", []):
        if candidate.get("verified") is not True:
            continue
        try:
            candidate_time = candidate_observed_at(candidate)
        except Exception:
            continue
        if candidate_time > feed_time + future_tolerance:
            continue
        if feed_time - candidate_time > max_age:
            continue

        profile_id = candidate.get("destination_profile_id")
        profile = by_id.get(profile_id)
        if not profile:
            continue
        if candidate.get("country") != profile.get("country"):
            continue
        if candidate.get("gateway_iata") != profile.get("gateway_iata"):
            continue
        if candidate.get("origin") != config["origin"]:
            continue
        if candidate.get("departure_date") != config["departure_date"]:
            continue
        if candidate.get("return_date") not in allowed_returns:
            continue
        if candidate.get("direct") is not True:
            continue

        time_text = candidate.get("return_departure_time")
        if not time_text:
            continue
        try:
            hour, minute = (int(x) for x in time_text.split(":", 1))
        except Exception:
            continue
        if hour < 0 or hour > 23 or minute < 0 or minute > 59:
            continue
        if (
            candidate.get("return_date") == "2026-10-02"
            and config.get("return_2026_10_02_morning_only") is True
            and hour >= 12
        ):
            continue

        if not isinstance(candidate.get("flight_total_ils"), (int, float)) or candidate["flight_total_ils"] <= 0:
            continue
        if not isinstance(candidate.get("hotel_total_ils"), (int, float)) or candidate["hotel_total_ils"] <= 0:
            continue
        if not isinstance(candidate.get("vacation_total_ils"), (int, float)) or candidate["vacation_total_ils"] <= 0:
            continue
        if not isinstance(candidate.get("stars"), (int, float)) or candidate["stars"] < config["hotel"]["min_stars"]:
            continue
        if not candidate.get("flight_url") or not candidate.get("hotel_url"):
            continue
        valid.append(candidate)

    return valid


def read_history():
    if not HISTORY.exists():
        return []
    records = []
    for raw in HISTORY.read_text(encoding="utf-8").splitlines():
        raw = raw.strip()
        if not raw:
            continue
        try:
            records.append(json.loads(raw))
        except json.JSONDecodeError:
            continue
    return records


def baseline_for(history, key, component, now):
    comparable = []
    for row in history:
        if row.get("key") != key or row.get("component") != component:
            continue
        try:
            observed = parse_iso(row["observed_at"])
            price = float(row["price_ils"])
        except Exception:
            continue
        if price > 0 and observed < now:
            comparable.append((observed, price))

    if not comparable:
        return None, 0

    recent = [price for observed, price in comparable if observed >= now - timedelta(days=7)]
    if recent:
        return statistics.median(recent), len(recent)

    older = sorted(comparable, key=lambda item: item[0], reverse=True)
    return older[0][1], 1


def detect_drops(valid_candidates, history, observed_at=None, threshold_pct=30):
    alerts = []
    existing_ids = {row.get("observation_id") for row in history}
    for c in valid_candidates:
        try:
            candidate_time = candidate_observed_at(c)
        except Exception:
            continue
        keys = component_keys(c)
        components = {
            "flight": float(c["flight_total_ils"]),
            "hotel": float(c["hotel_total_ils"]),
            "vacation": float(c["vacation_total_ils"]),
        }
        for component, current in components.items():
            obs_id = observation_id(c, keys[component], component)
            if obs_id in existing_ids:
                continue
            baseline, count = baseline_for(history, keys[component], component, candidate_time)
            if baseline is None or baseline <= 0:
                continue
            drop_pct = (baseline - current) / baseline * 100.0
            if drop_pct >= threshold_pct:
                alerts.append({
                    "observation_id": obs_id,
                    "stable_id": c.get("stable_id"),
                    "destination_profile_id": c["destination_profile_id"],
                    "destination": c["destination"],
                    "departure_date": c["departure_date"],
                    "return_date": c["return_date"],
                    "component": component,
                    "baseline_ils": round(baseline, 2),
                    "current_ils": round(current, 2),
                    "drop_pct": round(drop_pct, 1),
                    "history_observations": count,
                    "flight_url": c.get("flight_url"),
                    "hotel_url": c.get("hotel_url"),
                    "package_url": c.get("package_url"),
                })
    return alerts


def append_observations(valid_candidates, feed_verified_at=None, existing_history=None):
    existing_history = existing_history or []
    existing_ids = {row.get("observation_id") for row in existing_history}
    rows = []
    for c in valid_candidates:
        keys = component_keys(c)
        prices = {
            "flight": c["flight_total_ils"],
            "hotel": c["hotel_total_ils"],
            "vacation": c["vacation_total_ils"],
        }
        for component, price in prices.items():
            obs_id = observation_id(c, keys[component], component)
            if obs_id in existing_ids:
                continue
            existing_ids.add(obs_id)
            rows.append({
                "observation_id": obs_id,
                "observed_at": c["verified_at"],
                "key": keys[component],
                "component": component,
                "price_ils": round(float(price), 2),
                "destination_profile_id": c["destination_profile_id"],
                "destination": c["destination"],
                "departure_date": c["departure_date"],
                "return_date": c["return_date"],
                "source_provenance": c.get("source_provenance", []),
            })
    if rows:
        HISTORY.parent.mkdir(parents=True, exist_ok=True)
        with HISTORY.open("a", encoding="utf-8") as handle:
            for row in rows:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    return len(rows)


def rank_candidates(candidates):
    if not candidates:
        return []

    by_price = sorted(candidates, key=lambda c: float(c["vacation_total_ils"]))
    with_value = [c for c in candidates if isinstance(c.get("family_value"), (int, float))]
    best_value = max(with_value, key=lambda c: float(c["family_value"])) if with_value else by_price[0]
    picks = [("BEST VALUE", best_value)]

    cheapest = next((c for c in by_price if c is not best_value), None)
    if cheapest is not None:
        picks.append(("BEST PRICE", cheapest))

    used = {id(c) for _, c in picks}
    remaining = [c for c in candidates if id(c) not in used]
    if remaining:
        upgrade = max(
            remaining,
            key=lambda c: (
                float(c.get("family_value") or 0),
                float(c.get("stars") or 0),
                float(c.get("guest_score") or 0),
                -float(c["vacation_total_ils"]),
            ),
        )
        picks.append(("SMART UPGRADE / SURPRISE", upgrade))

    result = []
    for idx, (category, candidate) in enumerate(picks[:3], 1):
        item = dict(candidate)
        item["rank"] = idx
        item["category"] = category
        result.append(item)
    return result


def write_alert(alerts):
    if not alerts:
        ALERT.unlink(missing_ok=True)
        return
    component_names = {"flight": "טיסה", "hotel": "מלון", "vacation": "סה״כ חופשה"}
    lines = ["# 🚨 Sukkot 30%+ Price Drop", ""]
    for a in alerts:
        lines.append(
            f"- **{a['destination']}** {a['departure_date']}→{a['return_date']} · "
            f"{component_names[a['component']]}: ₪{a['baseline_ils']:,.0f} → ₪{a['current_ils']:,.0f} "
            f"(**-{a['drop_pct']:.1f}%**; baseline n={a['history_observations']})"
        )
        if a.get("flight_url"):
            lines.append(f"  - Flight: {a['flight_url']}")
        if a.get("hotel_url"):
            lines.append(f"  - Hotel: {a['hotel_url']}")
        if a.get("package_url"):
            lines.append(f"  - Package: {a['package_url']}")
    lines.extend(["", "Dashboard: https://yanivsa.github.io/family-travel-deal-monitor/"])
    ALERT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    config = load_json(CONFIG)
    whitelist = load_json(WHITELIST)
    feed = load_json(FEED)
    feed_verified_at = feed.get("verified_at")
    if not feed_verified_at:
        raise ValueError("provider feed is missing verified_at")

    valid_candidates = validate_feed(feed, config, whitelist)
    history_before = read_history()
    alerts = detect_drops(
        valid_candidates,
        history_before,
        threshold_pct=float(config.get("price_drop_threshold_pct", 30)),
    )
    appended = append_observations(valid_candidates, existing_history=history_before)

    coverage = feed.get("scan_coverage", {})
    data = {
        "generated_at": datetime.now(TZ).isoformat(),
        "timezone": "Asia/Jerusalem",
        "currency": "ILS",
        "search": config,
        "automation": {
            "status": coverage.get("status", "unknown"),
            "provider_mode": "feed-processing-only-no-live-collector",
            "last_attempt_at": feed_verified_at,
            "last_verified_live_refresh": max(
                (c.get("verified_at") for c in valid_candidates if c.get("verified_at")),
                default=None,
            ),
            "note": coverage.get("note", ""),
        },
        "scan_coverage": coverage,
        "provider_health": feed.get("provider_health", {}),
        "price_drop_alerts": alerts,
        "history_observations_added": appended,
        "deals": rank_candidates(valid_candidates),
    }
    DATA.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_alert(alerts)
    print(
        f"processed feed {feed_verified_at}: {len(valid_candidates)} fresh verified candidates, "
        f"{appended} new component observations, {len(alerts)} 30%+ alerts"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
