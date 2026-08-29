# Family Travel Deal Monitor

Repository rules are the source of truth for automated travel scans.

- Read `travel/config.json`, `travel/destination_whitelist.json`, and `travel/skills.json` before each scan or travel-search code change.
- Before changing search, ranking, normalization, history, or alert logic, ensure the upstream skills are synced with `python scripts/sync_travel_skills.py`, then read the relevant local `.agents/skills/<name>/SKILL.md` files.
- Required travel skills: `israeli-flight-finder`, `israeli-abroad-trip-planner`, `destination-compare`, `fare-watch`, and `hotel-search`. `rate-parity-monitor` is optional and should be used only when a supported live hotel-price source can honor its requirements.
- Repository rules and `travel/config.json` override any conflicting generic skill rule.
- Hard production scope is exactly one window: TLV departure `2026-09-27`, return `2026-10-02` before 12:00 local departure time. No 2026-10-01 results and no 2026-09-28 departures are production-eligible.
- Family occupancy is 2 adults + children ages 10, 7, 2 (API integer representation of the 2.5-year-old).
- Direct flights only. Turkey and Arab countries are excluded.
- Use only currently selected family-first destination profiles and their gateway airports. The collector must report actual gateway coverage and must never claim a gateway was checked when no live flight query completed.
- Live flight discovery/verification: prefer World Airfares; cross-check candidates with eDreams/Skyscanner when practical. Direct flights only.
- Live hotel verification: Booking.com is primary; eDreams/BreckenWander may cross-check.
- eDreams must also be considered for real Flight+Hotel/package pricing when the available connector exposes a verifiable bundle price; never label a manually summed flight+hotel as an official eDreams package.
- Never invent price, availability, baggage, room details, rating, package status or booking URL.
- Persist every collector cycle to `travel/provider-feed.json` with provider health and explicit scan coverage, even when no alert fires.
- Track flight, hotel, package, and vacation totals separately. A new observation without history is NEW, not PRICE DROP.
- PRICE DROP alert threshold is 30% or more versus sufficient comparable history for the same stable product and the same hard date window. Compare flight, hotel, and vacation total independently.
- Production architecture is hybrid until equivalent provider API credentials exist inside GitHub Actions: scheduled live collector using the connected travel tools -> `travel/provider-feed.json` -> GitHub Actions validation/history/30% detection -> Pages/Issue alert. Jules is not an hourly runtime.
- A 30%+ verified alert may be emailed by the scheduled collector through the connected Gmail account. Do not send routine hourly emails.
