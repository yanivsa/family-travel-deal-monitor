# Family Travel Deal Monitor

Repository rules are the source of truth for automated travel scans.

- Read `travel/config.json`, `travel/destination_whitelist.json`, and `travel/skills.json` before each scan or travel-search code change.
- Before changing search, ranking, normalization, history, or alert logic, ensure the upstream skills are synced with `python scripts/sync_travel_skills.py`, then read the relevant local `.agents/skills/<name>/SKILL.md` files.
- Required travel skills: `israeli-flight-finder`, `israeli-abroad-trip-planner`, `destination-compare`, `fare-watch`, and `hotel-search`. `rate-parity-monitor` is optional and should be used only when a supported live hotel-price source can honor its requirements.
- Repository rules and `travel/config.json` override any conflicting generic skill rule.
- Use only whitelist destinations and their gateway airports.
- Live flight discovery/verification: prefer World Airfares; cross-check candidates with eDreams/Skyscanner when practical. Direct flights only.
- Live hotel verification: Booking.com is primary; eDreams/BreckenWander may cross-check.
- eDreams must also be considered for real Flight+Hotel/package pricing when the available connector exposes a verifiable bundle price; never label a manually summed flight+hotel as an official eDreams package.
- Never invent price, availability, baggage, room details, rating, package status or booking URL.
- Persist every run to `travel/provider-feed.json` with provider health and explicit scan coverage, even when no alert fires.
- Track flight, hotel, package, and vacation totals separately. A new observation without history is NEW, not PRICE DROP.
- PRICE DROP alert threshold is 30% or more versus sufficient comparable history for the same stable product/date window. Compare flight, hotel, and vacation total independently.
- Final production alerts must be sent autonomously by GitHub Actions/email infrastructure built in this repository; ChatGPT automation is only a temporary fallback until E2E email delivery is proven.
