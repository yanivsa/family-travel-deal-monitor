# Family Travel Deal Monitor

Repository rules are the source of truth for automated travel scans.

- Read `travel/config.json` and `travel/destination_whitelist.json` before each scan.
- Use only whitelist destinations and their gateway airports.
- Live flight discovery/verification: prefer World Airfares; cross-check candidates with eDreams/Skyscanner when practical. Direct flights only.
- Live hotel verification: Booking.com is primary; eDreams/BreckenWander may cross-check.
- Never invent price, availability, baggage, room details, rating, package status or booking URL.
- Persist every run to `travel/provider-feed.json` with provider health, even when no alert fires.
- Track flight, hotel and vacation totals separately. A new observation without history is NEW, not PRICE DROP.
- PRICE DROP alert threshold is 30% or more versus sufficient comparable history for the same stable product/date window.
- Apply the relevant workflow principles from `skills-il/travel/israeli-flight-finder` and `skills-il/travel/israeli-abroad-trip-planner`; repository rules override conflicts.
