# Jules implementation task

Implement authorized live provider adapters for the hourly Sukkot 2026 family travel monitor in this repository.

Hard constraints:
- Family: 2 adults + 3 children ages 10, 7, 2.
- Dates only: 2026-09-27 or 2026-09-28 outbound; 2026-10-01 or 2026-10-02 morning return.
- Exclude Turkey and Arab countries.
- Exactly 3 ranked outputs: BEST VALUE, BEST PRICE, SMART UPGRADE / SURPRISE.
- Primary verification: live flight + hotel booking sources. Never fabricate unavailable data.
- Preserve last-known-good data if any provider fails.
- Calculate Effective Vacation Time and Family Value using the scoring policy documented in the issue.
- Use GitHub Actions Secrets for credentials; never commit secrets.
- Add tests for date guards, excluded destinations, ranking, Time Value and price-drop detection.

Preferred adapters when authorized programmatic access exists: World Airfares, Booking.com, Skyscanner, eDreams, BreckenWander. Social/community sources are discovery-only; prices shown in Top 3 must be live-verified.

The public dashboard must remain at https://yanivsa.github.io/family-travel-deal-monitor/ and the hourly workflow must remain autonomous.
