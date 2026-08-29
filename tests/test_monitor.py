from datetime import datetime
from zoneinfo import ZoneInfo

import monitor

TZ = ZoneInfo("Asia/Jerusalem")


def load_contract():
    return monitor.load_json(monitor.CONFIG), monitor.load_json(monitor.WHITELIST)


def valid_candidate(return_date="2026-10-02", return_time="08:20", verified_at="2026-08-29T22:00:00+03:00"):
    return {
        "stable_id": "fixture-1",
        "destination_profile_id": "cy-larnaca",
        "destination": "Larnaca",
        "country": "Cyprus",
        "gateway_iata": "LCA",
        "origin": "TLV",
        "departure_date": "2026-09-27",
        "return_date": return_date,
        "return_departure_time": return_time,
        "direct": True,
        "airline": "Fixture Air",
        "flight_total_ils": 5000.0,
        "baggage": "Cabin bag only",
        "flight_url": "https://example.test/flight",
        "hotel": "Fixture Family Hotel",
        "stars": 4,
        "guest_score": 8.5,
        "rooms": 1,
        "hotel_total_ils": 4000.0,
        "hotel_url": "https://example.test/hotel",
        "vacation_total_ils": 9000.0,
        "verified": True,
        "verified_at": verified_at,
        "source_provenance": ["fixture"],
    }


def feed_with(candidate, feed_verified_at="2026-08-29T22:00:00+03:00"):
    config, whitelist = load_contract()
    return {
        "verified_at": feed_verified_at,
        "config": {
            "origin": config["origin"],
            "departure_date": config["departure_date"],
            "return_dates": config["return_dates"],
            "direct_only": True,
            "party": config["party"],
        },
        "scan_coverage": {
            "whitelist_profiles": len(whitelist),
            "unique_gateways_total": len({x["gateway_iata"] for x in whitelist}),
            "gateways_live_checked_this_run": ["LCA"],
        },
        "provider_health": {},
        "candidates": [candidate],
    }


def test_whitelist_contract_is_exactly_64_profiles_and_48_gateways():
    _, whitelist = load_contract()
    assert len(whitelist) == 64
    assert len({item["gateway_iata"] for item in whitelist}) == 48
    ayia = next(x for x in whitelist if x["id"] == "cy-ayia-napa")
    assert ayia["gateway_iata"] == "LCA"


def test_current_provider_feed_coverage_metadata_matches_whitelist():
    _, whitelist = load_contract()
    feed = monitor.load_json(monitor.FEED)
    coverage = feed["scan_coverage"]
    assert coverage["whitelist_profiles"] == len(whitelist) == 64
    assert coverage["unique_gateways_total"] == len({x["gateway_iata"] for x in whitelist}) == 48
    assert set(coverage["gateways_live_checked_this_run"]).issubset({x["gateway_iata"] for x in whitelist})


def test_current_date_and_direct_contract():
    config, _ = load_contract()
    assert config["departure_date"] == "2026-09-27"
    assert config["return_dates"] == ["2026-10-02"]
    assert config["return_2026_10_02_morning_only"] is True
    assert config["direct_only"] is True
    assert config["party"] == {"adults": 2, "children_ages": [10, 7, 2]}
    assert config["price_drop_threshold_pct"] == 30
    assert config["max_candidate_age_minutes"] == 90


def test_valid_direct_candidate_is_accepted():
    config, whitelist = load_contract()
    candidate = valid_candidate()
    assert monitor.validate_feed(feed_with(candidate), config, whitelist) == [candidate]


def test_departure_28_september_is_rejected():
    config, whitelist = load_contract()
    candidate = valid_candidate()
    candidate["departure_date"] = "2026-09-28"
    assert monitor.validate_feed(feed_with(candidate), config, whitelist) == []


def test_october_1_is_rejected():
    config, whitelist = load_contract()
    candidate = valid_candidate(return_date="2026-10-01", return_time="16:00")
    assert monitor.validate_feed(feed_with(candidate), config, whitelist) == []


def test_connection_is_rejected():
    config, whitelist = load_contract()
    candidate = valid_candidate()
    candidate["direct"] = False
    assert monitor.validate_feed(feed_with(candidate), config, whitelist) == []


def test_october_2_noon_or_later_is_rejected():
    config, whitelist = load_contract()
    candidate = valid_candidate(return_time="12:00")
    assert monitor.validate_feed(feed_with(candidate), config, whitelist) == []


def test_october_2_morning_is_accepted():
    config, whitelist = load_contract()
    candidate = valid_candidate(return_time="11:59")
    assert monitor.validate_feed(feed_with(candidate), config, whitelist) == [candidate]


def test_candidate_older_than_90_minutes_is_rejected():
    config, whitelist = load_contract()
    candidate = valid_candidate(verified_at="2026-08-29T20:29:59+03:00")
    feed = feed_with(candidate, feed_verified_at="2026-08-29T22:00:00+03:00")
    assert monitor.validate_feed(feed, config, whitelist) == []


def test_candidate_at_90_minute_boundary_is_accepted():
    config, whitelist = load_contract()
    candidate = valid_candidate(verified_at="2026-08-29T20:30:00+03:00")
    feed = feed_with(candidate, feed_verified_at="2026-08-29T22:00:00+03:00")
    assert monitor.validate_feed(feed, config, whitelist) == [candidate]


def history_for(candidate, component, baseline):
    keys = monitor.component_keys(candidate)
    return [{
        "observed_at": "2026-08-28T10:00:00+03:00",
        "key": keys[component],
        "component": component,
        "price_ils": baseline,
    }]


def test_29_9_percent_drop_does_not_alert():
    candidate = valid_candidate()
    candidate["flight_total_ils"] = 70.1
    candidate["vacation_total_ils"] = 4070.1
    alerts = monitor.detect_drops([candidate], history_for(candidate, "flight", 100.0), threshold_pct=30.0)
    assert not [a for a in alerts if a["component"] == "flight"]


def test_exact_30_percent_drop_alerts():
    candidate = valid_candidate()
    candidate["flight_total_ils"] = 70.0
    candidate["vacation_total_ils"] = 4070.0
    alerts = monitor.detect_drops([candidate], history_for(candidate, "flight", 100.0), threshold_pct=30.0)
    flight_alerts = [a for a in alerts if a["component"] == "flight"]
    assert len(flight_alerts) == 1
    assert flight_alerts[0]["drop_pct"] == 30.0


def test_same_component_observation_does_not_alert_twice():
    candidate = valid_candidate()
    candidate["flight_total_ils"] = 70.0
    candidate["vacation_total_ils"] = 4070.0
    keys = monitor.component_keys(candidate)
    history = history_for(candidate, "flight", 100.0)
    history.append({
        "observation_id": monitor.observation_id(candidate, keys["flight"], "flight"),
        "observed_at": candidate["verified_at"],
        "key": keys["flight"],
        "component": "flight",
        "price_ils": 70.0,
    })
    alerts = monitor.detect_drops([candidate], history, threshold_pct=30.0)
    assert not [a for a in alerts if a["component"] == "flight"]


def test_component_history_keys_are_independent():
    candidate = valid_candidate()
    keys = monitor.component_keys(candidate)
    assert keys["flight"] != keys["hotel"] != keys["vacation"]
    assert keys["flight"].endswith("|direct")


def test_rank_categories_are_unique_and_do_not_fabricate_results():
    one = valid_candidate()
    ranked = monitor.rank_candidates([one])
    assert len(ranked) == 1
    assert ranked[0]["category"] == "BEST VALUE"
