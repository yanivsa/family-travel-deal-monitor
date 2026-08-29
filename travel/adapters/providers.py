"""
Authorized provider adapters for World Airfares, Booking.com, Skyscanner, eDreams, BreckenWander, and JSON URL.
All adapters utilize credentials strictly from GitHub Actions Secrets / Environment Variables.
Never scrape or bypass anti-bot protections.
If credentials or API requests fail, adapters safely return empty candidate lists so last-known-good data is preserved.
"""

import json
import os
import urllib.request
import urllib.parse
from typing import List, Dict, Any
from travel.adapters.base import BaseProviderAdapter, DISCOVERY_DESTINATIONS, SEARCH_WINDOWS, FAMILY_PASSENGERS
from travel.guards import validate_deal_guards
from travel.scoring import calculate_evt_hours, get_time_value, calculate_family_value

class WorldAirfaresAdapter(BaseProviderAdapter):
    def __init__(self):
        super().__init__("World Airfares")
        self.api_key = os.getenv("WORLD_AIRFARES_API_KEY", "").strip()
        self.endpoint = os.getenv("WORLD_AIRFARES_ENDPOINT", "https://api.worldairfares.com/v1/search").strip()

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def fetch_candidates(self) -> List[Dict[str, Any]]:
        if not self.is_configured():
            return []
        candidates = []
        try:
            req = urllib.request.Request(
                self.endpoint,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "User-Agent": "family-travel-deal-monitor/1.0"
                }
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.load(resp)
                for item in data.get("flights", []):
                    candidates.append(item)
        except Exception:
            pass
        return candidates

class BookingComAdapter(BaseProviderAdapter):
    def __init__(self):
        super().__init__("Booking.com")
        self.api_key = os.getenv("BOOKING_COM_API_KEY", "").strip()
        self.endpoint = os.getenv("BOOKING_COM_ENDPOINT", "https://distribution-xml.booking.com/2.4/json/hotelAvailability").strip()

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def fetch_candidates(self) -> List[Dict[str, Any]]:
        if not self.is_configured():
            return []
        candidates = []
        try:
            req = urllib.request.Request(
                self.endpoint,
                headers={
                    "X-Api-Key": self.api_key,
                    "User-Agent": "family-travel-deal-monitor/1.0"
                }
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.load(resp)
                for item in data.get("hotels", []):
                    candidates.append(item)
        except Exception:
            pass
        return candidates

class SkyscannerAdapter(BaseProviderAdapter):
    def __init__(self):
        super().__init__("Skyscanner")
        self.api_key = os.getenv("SKYSCANNER_API_KEY", "").strip()
        self.endpoint = os.getenv("SKYSCANNER_ENDPOINT", "https://partners.api.skyscanner.net/apiservices/v3/flights/live/search/synced").strip()

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def fetch_candidates(self) -> List[Dict[str, Any]]:
        if not self.is_configured():
            return []
        candidates = []
        try:
            req = urllib.request.Request(
                self.endpoint,
                headers={
                    "x-api-key": self.api_key,
                    "Content-Type": "application/json"
                }
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.load(resp)
                for item in data.get("itineraries", []):
                    candidates.append(item)
        except Exception:
            pass
        return candidates

class EDreamsAdapter(BaseProviderAdapter):
    def __init__(self):
        super().__init__("eDreams")
        self.api_key = os.getenv("EDREAMS_API_KEY", "").strip()
        self.endpoint = os.getenv("EDREAMS_ENDPOINT", "https://api.edreams.com/v1/packages/search").strip()

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def fetch_candidates(self) -> List[Dict[str, Any]]:
        if not self.is_configured():
            return []
        candidates = []
        try:
            req = urllib.request.Request(
                self.endpoint,
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.load(resp)
                for item in data.get("packages", []):
                    candidates.append(item)
        except Exception:
            pass
        return candidates

class BreckenWanderAdapter(BaseProviderAdapter):
    def __init__(self):
        super().__init__("BreckenWander")
        self.api_key = os.getenv("BRECKENWANDER_API_KEY", "").strip()
        self.endpoint = os.getenv("BRECKENWANDER_ENDPOINT", "https://api.breckenwander.com/v1/deals").strip()

    def is_configured(self) -> bool:
        return bool(self.api_key)

    def fetch_candidates(self) -> List[Dict[str, Any]]:
        if not self.is_configured():
            return []
        candidates = []
        try:
            req = urllib.request.Request(
                self.endpoint,
                headers={"X-Brecken-Token": self.api_key}
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.load(resp)
                for item in data.get("deals", []):
                    candidates.append(item)
        except Exception:
            pass
        return candidates

class GenericJsonUrlAdapter(BaseProviderAdapter):
    def __init__(self):
        super().__init__("Generic JSON Provider URL")
        self.url = os.getenv("TRAVEL_PROVIDER_JSON_URL", "").strip()

    def is_configured(self) -> bool:
        return bool(self.url)

    def fetch_candidates(self) -> List[Dict[str, Any]]:
        if not self.is_configured():
            return []
        try:
            req = urllib.request.Request(
                self.url,
                headers={"User-Agent": "family-travel-deal-monitor/1.0"}
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.load(resp)
                return data.get("deals", [])
        except Exception:
            return []

def aggregate_provider_deals() -> List[Dict[str, Any]]:
    """
    Executes all configured authorized adapters and collects verified deal candidates.
    Calculates EVT, Time Value, and Family Value scores for each candidate.
    Filters candidates using date and destination guards.
    """
    adapters = [
        WorldAirfaresAdapter(),
        BookingComAdapter(),
        SkyscannerAdapter(),
        EDreamsAdapter(),
        BreckenWanderAdapter(),
        GenericJsonUrlAdapter()
    ]

    all_raw_candidates = []
    for adapter in adapters:
        if adapter.is_configured():
            candidates = adapter.fetch_candidates()
            all_raw_candidates.extend(candidates)

    verified_deals = []
    for deal in all_raw_candidates:
        valid, reason = validate_deal_guards(deal)
        if not valid:
            continue

        if not deal.get("verified", True):
            continue

        if not deal.get("flight_url") or not deal.get("hotel_url"):
            continue

        total_ils = deal.get("total_ils")
        if not isinstance(total_ils, (int, float)) or total_ils <= 0:
            continue

        # Compute EVT & Scoring if missing
        dep_date = deal.get("departure_date") or "2026-09-28"
        ret_date = deal.get("return_date") or "2026-10-01"
        outbound = deal.get("outbound", "08:00 → 10:00")
        ret_flight = deal.get("return", "08:00 → 10:00")

        evt = deal.get("effective_vacation_hours")
        if evt is None:
            evt = calculate_evt_hours(dep_date, ret_date, outbound, ret_flight)
            deal["effective_vacation_hours"] = evt

        if not deal.get("time_value"):
            deal["time_value"] = get_time_value(evt)

        if not deal.get("family_value"):
            deal["family_value"] = calculate_family_value(deal)

        verified_deals.append(deal)

    return verified_deals
