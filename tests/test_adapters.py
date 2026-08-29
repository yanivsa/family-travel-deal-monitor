"""
Integration tests for authorized provider adapters using mock fixtures to avoid paid API calls in CI.
"""

import json
import os
import pytest
from unittest.mock import patch, MagicMock
from travel.adapters.providers import (
    WorldAirfaresAdapter,
    BookingComAdapter,
    SkyscannerAdapter,
    EDreamsAdapter,
    BreckenWanderAdapter,
    GenericJsonUrlAdapter,
    aggregate_provider_deals
)

def test_provider_adapters_not_configured_by_default(monkeypatch):
    monkeypatch.delenv("WORLD_AIRFARES_API_KEY", raising=False)
    monkeypatch.delenv("BOOKING_COM_API_KEY", raising=False)
    monkeypatch.delenv("SKYSCANNER_API_KEY", raising=False)
    monkeypatch.delenv("EDREAMS_API_KEY", raising=False)
    monkeypatch.delenv("BRECKENWANDER_API_KEY", raising=False)
    monkeypatch.delenv("TRAVEL_PROVIDER_JSON_URL", raising=False)

    assert WorldAirfaresAdapter().is_configured() is False
    assert BookingComAdapter().is_configured() is False
    assert SkyscannerAdapter().is_configured() is False
    assert EDreamsAdapter().is_configured() is False
    assert BreckenWanderAdapter().is_configured() is False
    assert GenericJsonUrlAdapter().is_configured() is False

    # Aggregate yields empty list without credentials and does not raise exception
    candidates = aggregate_provider_deals()
    assert candidates == []

def test_world_airfares_adapter_with_mock_fixture(monkeypatch):
    monkeypatch.setenv("WORLD_AIRFARES_API_KEY", "mock-key-123")
    adapter = WorldAirfaresAdapter()
    assert adapter.is_configured() is True

    mock_response = MagicMock()
    mock_response.__enter__.return_value.read.return_value = b'{"flights": [{"destination": "Larnaca, Cyprus", "total_ils": 5000}]}'

    with patch("urllib.request.urlopen", return_value=mock_response):
        results = adapter.fetch_candidates()
        assert len(results) == 1
        assert results[0]["destination"] == "Larnaca, Cyprus"

def test_generic_json_url_adapter_with_mock_fixture(monkeypatch):
    monkeypatch.setenv("TRAVEL_PROVIDER_JSON_URL", "https://mock.example.com/deals.json")
    adapter = GenericJsonUrlAdapter()
    assert adapter.is_configured() is True

    mock_deal = {
        "rank": 1,
        "category": "BEST VALUE",
        "destination": "איה נאפה, קפריסין",
        "departure_date": "2026-09-28",
        "return_date": "2026-10-02",
        "return_morning": True,
        "outbound": "06:20 → 07:20",
        "return": "08:20 → 09:20",
        "flight_url": "https://example.com/flight",
        "hotel_url": "https://example.com/hotel",
        "total_ils": 9900,
        "verified": True
    }
    mock_json = f'{{"deals": [{json.dumps(mock_deal)}]}}'.encode("utf-8")

    mock_response = MagicMock()
    mock_response.__enter__.return_value.read.return_value = mock_json

    with patch("urllib.request.urlopen", return_value=mock_response):
        deals = aggregate_provider_deals()
        assert len(deals) == 1
        assert deals[0]["destination"] == "איה נאפה, קפריסין"
        assert deals[0]["effective_vacation_hours"] > 80
