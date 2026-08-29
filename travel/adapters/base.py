"""
Base provider adapter interface and discovery engine.
Defines candidate search structures across 12-20 Mediterranean and European family destinations.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

# 12-20 Allowed family destinations across Cyprus, Greece, Italy, Spain, Central Europe
DISCOVERY_DESTINATIONS = [
    {"code": "LCA", "city": "לרנקה", "country": "קפריסין"},
    {"code": "PFO", "city": "פאפוס", "country": "קפריסין"},
    {"code": "AYN", "city": "איה נאפה", "country": "קפריסין"},
    {"code": "HER", "city": "כרתים / הרסוניסוס", "country": "יוון"},
    {"code": "RHO", "city": "רודוס", "country": "יוון"},
    {"code": "ATH", "city": "אתונה", "country": "יוון"},
    {"code": "SKG", "city": "סלוניקי / חלקידיקי", "country": "יוון"},
    {"code": "CFU", "city": "קורפו", "country": "יוון"},
    {"code": "FCO", "city": "רומא", "country": "איטליה"},
    {"code": "MXP", "city": "מילאנו / אגמים", "country": "איטליה"},
    {"code": "BCN", "city": "ברצלונה / קוסטה בראווה", "country": "ספרד"},
    {"code": "PMI", "city": "פאלמה דה מיורקה", "country": "ספרד"},
    {"code": "BUD", "city": "בודפשט", "country": "הונגריה"},
    {"code": "PRG", "city": "פראג", "country": "צ'כיה"},
    {"code": "VIE", "city": "וינה", "country": "אוסטריה"},
    {"code": "TGD", "city": "מונטנגרו", "country": "מונטנגרו"},
]

SEARCH_WINDOWS = [
    {"outbound": "2026-09-27", "return": "2026-10-01", "return_morning": False},
    {"outbound": "2026-09-27", "return": "2026-10-02", "return_morning": True},
    {"outbound": "2026-09-28", "return": "2026-10-01", "return_morning": False},
    {"outbound": "2026-09-28", "return": "2026-10-02", "return_morning": True},
]

FAMILY_PASSENGERS = {
    "adults": 2,
    "children_ages": [10, 7, 2],
    "total_pax": 5
}

class BaseProviderAdapter(ABC):
    """Abstract Base Class for authorized travel provider adapters."""

    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def is_configured(self) -> bool:
        """Returns True if official secrets/credentials or endpoints are configured."""
        pass

    @abstractmethod
    def fetch_candidates(self) -> List[Dict[str, Any]]:
        """
        Fetches live candidates from official API.
        Must return list of candidate deal dicts matching schema.
        If credentials missing or API fails, returns empty list.
        """
        pass
