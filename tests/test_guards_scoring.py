"""
Unit tests for date guards, excluded destinations, scoring, and price history detection.
"""

import pytest
from travel.guards import is_allowed_date_pair, is_morning_return, is_destination_excluded, validate_deal_guards
from travel.scoring import calculate_evt_hours, get_time_value, calculate_family_value
from travel.price_history import detect_meaningful_changes

def test_allowed_date_pairs():
    assert is_allowed_date_pair("2026-09-27", "2026-10-01") is True
    assert is_allowed_date_pair("2026-09-27", "2026-10-02") is True
    assert is_allowed_date_pair("2026-09-28", "2026-10-01") is True
    assert is_allowed_date_pair("2026-09-28", "2026-10-02") is True

    # Disallowed dates
    assert is_allowed_date_pair("2026-09-26", "2026-10-01") is False
    assert is_allowed_date_pair("2026-09-27", "2026-10-03") is False

def test_morning_return_guard():
    # 2026-10-01 return does not require morning check
    assert is_morning_return("2026-10-01", "18:00 → 19:00") is True

    # 2026-10-02 return requires morning departure (< 12:00)
    assert is_morning_return("2026-10-02", "08:20 → 09:20") is True
    assert is_morning_return("2026-10-02", "14:00 → 15:00") is False
    assert is_morning_return("2026-10-02", return_morning_flag=True) is True

def test_excluded_destinations():
    assert is_destination_excluded("Istanbul, Turkey") is True
    assert is_destination_excluded("Sharm El Sheikh, Egypt") is True
    assert is_destination_excluded("Dubai, UAE") is True
    assert is_destination_excluded("Larnaca, Cyprus") is False
    assert is_destination_excluded("Heraklion, Greece") is False

def test_validate_deal_guards():
    valid_deal = {
        "departure_date": "2026-09-28",
        "return_date": "2026-10-02",
        "return": "08:20 → 09:20",
        "destination": "Larnaca, Cyprus",
        "total_ils": 8000,
        "flight_url": "https://example.com/flight",
        "hotel_url": "https://example.com/hotel"
    }
    valid, msg = validate_deal_guards(valid_deal)
    assert valid is True

    excluded_deal = dict(valid_deal)
    excluded_deal["destination"] = "Antalya, Turkey"
    valid, msg = validate_deal_guards(excluded_deal)
    assert valid is False

    invalid_date_deal = dict(valid_deal)
    invalid_date_deal["departure_date"] = "2026-09-25"
    valid, msg = validate_deal_guards(invalid_date_deal)
    assert valid is False

def test_evt_and_time_value():
    evt = calculate_evt_hours("2026-09-28", "2026-10-02", "06:20 → 07:20", "08:20 → 09:20")
    assert evt > 80
    assert get_time_value(evt) == "מצוין"
    assert get_time_value(70) == "טוב"
    assert get_time_value(50) == "סביר"

def test_family_value_score():
    deal = {
        "total_ils": 8000,
        "effective_vacation_hours": 90,
        "stars": 4,
        "guest_score": 8.5,
        "direct": True,
        "family_benefits": ["Kids club", "Pool"]
    }
    score = calculate_family_value(deal)
    assert 50 <= score <= 100

def test_price_history_drop_detection():
    old_data = {
        "deals": [
            {"category": "BEST VALUE", "destination": "Cyprus", "total_ils": 10000, "effective_vacation_hours": 90}
        ]
    }
    new_data = {
        "deals": [
            {"category": "BEST VALUE", "destination": "Cyprus", "total_ils": 9500, "effective_vacation_hours": 90}
        ]
    }
    changes = detect_meaningful_changes(old_data, new_data)
    assert len(changes) == 1
    assert "PRICE DROP" in changes[0]
