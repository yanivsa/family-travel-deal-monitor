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
- eDreams must also be considered for real Flight+Hotel/package pricing when an authorized GitHub-accessible provider/API returns a verifiable bundle price; never label a manually summed flight+hotel as an official eDreams package.
- Never invent price, availability, baggage, room details, rating, package status or booking URL.
- Persist every collector cycle to `travel/provider-feed.json` with provider health and explicit scan coverage, even when no alert fires.
- Track flight, hotel, package, and vacation totals separately. A new observation without history is NEW, not PRICE DROP.
- PRICE DROP alert threshold is 30% or more versus sufficient comparable history for the same stable product and the same hard date window. Compare flight, hotel, and vacation total independently.
- Production runtime must be GitHub-only: scheduled GitHub Actions live collector -> `travel/provider-feed.json` -> validation/history/30% detection -> Pages deployment -> optional GitHub alert/email. ChatGPT automations and ChatGPT connector sessions are forbidden as production runtime. Jules builds and maintains the code but is not the recurring runtime.
- If a provider cannot be queried from GitHub without a credential or supported bridge, report it truthfully as `not_configured`/`unsupported` and document the exact one-time setup required. Never replace a missing provider with a speculative endpoint.
- A verified 30%+ alert may be emailed from GitHub Actions through a supported secret-backed mail transport only after a successful E2E test. Do not send routine hourly emails.
