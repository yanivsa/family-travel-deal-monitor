import os
import tempfile
from pathlib import Path
from travel.collector import LiveCollector, get_unique_gateways, load_json, CONFIG_PATH, WHITELIST_PATH


def test_unique_gateways_count_is_48_from_64_whitelist_profiles():
    whitelist = load_json(WHITELIST_PATH)
    assert len(whitelist) == 64
    gateways = get_unique_gateways(whitelist)
    assert len(gateways) == 48
    assert "LCA" in gateways
    assert "ATH" in gateways
    assert "CDG" in gateways


def test_collector_search_scope_and_config():
    config = load_json(CONFIG_PATH)
    assert config["origin"] == "TLV"
    assert config["departure_date"] == "2026-09-27"
    assert config["return_dates"] == ["2026-10-01", "2026-10-02"]
    assert config["return_2026_10_02_morning_only"] is True
    assert config["direct_only"] is True
    assert config["party"] == {"adults": 2, "children_ages": [10, 7, 2]}


def test_provider_credentials_check_when_unconfigured(monkeypatch):
    for env_var in ["WORLD_AIRFARES_API_KEY", "BOOKING_API_KEY", "SKYSCANNER_API_KEY", "EDREAMS_API_KEY"]:
        monkeypatch.delenv(env_var, raising=False)

    collector = LiveCollector()
    health = collector.check_provider_credentials()
    assert health["World Airfares"]["status"] == "not_configured"
    assert health["Booking.com"]["status"] == "not_configured"
    assert health["Skyscanner"]["status"] == "unsupported"
    assert health["eDreams"]["status"] == "unsupported"


def test_provider_credentials_check_when_configured(monkeypatch):
    monkeypatch.setenv("WORLD_AIRFARES_API_KEY", "test_key_123")
    collector = LiveCollector()
    health = collector.check_provider_credentials()
    assert health["World Airfares"]["status"] == "ok"


def test_collect_writes_truthful_feed_coverage_and_48_gateways():
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_feed = Path(tmpdir) / "provider-feed.json"

        collector = LiveCollector(feed_path=tmp_feed)
        feed = collector.collect()

        assert tmp_feed.exists()
        assert feed["scan_coverage"]["whitelist_profiles"] == 64
        assert feed["scan_coverage"]["unique_gateways_total"] == 48
        assert len(feed["scan_coverage"]["gateways_live_checked_this_run"]) == 48
        assert "LCA" in feed["scan_coverage"]["gateways_live_checked_this_run"]
        assert feed["config"]["origin"] == "TLV"
        assert feed["config"]["departure_date"] == "2026-09-27"
