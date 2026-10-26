---
name: israeli-flight-finder
description: "Compare real flight prices from Ben Gurion (TLV): build pre-filled search links for Google Flights, Skyscanner, and KAYAK for the traveler's exact route and dates, read the live fares off them, and add Israeli-airline baggage for a true total cost. Use when someone asks to find or compare cheap flights from Israel, wants the cheapest fare or the cheapest dates to fly, or asks about El Al, Israir, Arkia, or Wizz Air baggage fees, seasonal TLV pricing, Issta flight+hotel packages, or whether to buy a ticket from the airline, an Israeli agency, or a foreign booking site such as Rift (formerly Soar). Presents a real comparison and never quotes invented prices. Do NOT use for domestic travel within Israel (use israeli-travel-planner), train schedules (use railil), or hotel-only bookings."
license: MIT
---

# Israeli Flight Finder

Find the cheapest flights from Ben Gurion Airport (TLV) by building a real, live price comparison for the traveler's exact route and dates, then reading the current fares off the search platforms. This skill does the comparison; it does not just list websites.

> **TLV carrier status is highly volatile (verified late October 2026).** The Iran war that began on 28 February 2026 shut Israeli airspace to most foreign airlines; Ben Gurion partially reopened in early March for Israeli carriers and has been fully open since 9 April 2026. Most foreign carriers are back, a few stay suspended into 2027, and a single incident can still pull a carrier overnight (flydubai suspended all Israel flights on 30 September 2026). Treat every carrier status in this skill as a dated snapshot, not a guarantee. That is why "How to Search" builds a live search for the traveler's own dates, and why you confirm the specific airline and route on its own site before relying on it.

## Comparison Platforms

Use multiple platforms -- each has different strengths. Never rely on a single source.

| Platform | URL | Strengths |
|----------|-----|-----------|
| Google Flights | google.com/travel/flights?gl=IL&hl=he | Direct airline prices, price tracking, "Explore" map, fare history graphs |
| Skyscanner | skyscanner.co.il | Broad airline and OTA coverage, "Everywhere" search, monthly price calendar |
| KAYAK | il.kayak.com | Price alerts, flexible date search |
| Issta | issta.co.il | Israeli travel agency, flight+hotel packages, Hebrew service |
| Lametayel | lametayel.co.il | Israeli travel site with flight comparison |

Start with Google Flights (direct airline prices) and cross-check Skyscanner (OTA deals); use Skyscanner "Everywhere" or the Google Flights "Explore" map for "anywhere cheap", Issta for flight+hotel packages, and Google Flights or KAYAK for price alerts. Per-platform detail: `references/comparison-platforms.md`.

## Israeli Airlines

### El Al (LY) -- Flag Carrier

- **Hub**: Ben Gurion (TLV)
- **Network**: El Al's summer 2026 schedule, announced before the war, planned about 900 weekly flights to 50+ destinations and a record 55 weekly to North America. For winter 2026-27 it runs 45 weekly flights to six US destinations, including San Francisco.
- **Website**: elal.com
- **Does not fly Shabbat**: El Al does not fly passengers on Shabbat or Jewish holidays - see "Shabbat-Aware Scheduling" below before planning return flights.
- **Frequent flyer**: Matmid, whose program has four tier statuses above base membership (Silver, Gold, Platinum, Top Platinum). You advance by earning "Diamonds", the more Diamonds, the faster you climb.

**Baggage policy (verified October 2026 on elal.com):**

| Fare class | Carry-on | Checked bags |
|------------|----------|--------------|
| Economy Lite | 1 x 8 kg (56x45x25 cm) + 1 personal item (gate-checked on Europe/UAE, below) | None included (paid add-on) |
| Economy Classic | 1 x 8 kg + 1 personal item | 1 x 23 kg |
| Economy Flex | 2 carry-ons, 8 kg each (12 kg total) + 1 personal item | 1 x 23 kg (2 x 23 kg to the Far East and Africa) |
| Premium | 2 carry-ons, 8 kg each (12 kg total) + 1 personal item | 2 x 23 kg |
| Business | 2 carry-ons, 16 kg each (20 kg total) + 1 personal item | 2 x 32 kg |

**Economy Lite restriction (Europe/UAE)**: Since 21 May 2025, Lite passengers on flights to/from Europe or the UAE must send their carry-on to the hold at the gate (free). Only a personal item (38x30x18 cm) stays in the cabin. Matmid members with Silver status or higher are exempt. North America routes sell only Classic and Flex, and on flights departing the US, TSA rules allow one carry-on plus one personal item in the cabin. Extra bags bought online cost up to 50% less than at the airport.

### Israir (6H)

- **Hub**: Ben Gurion (TLV)
- **Network**: Europe and Mediterranean leisure routes plus New York JFK (new route, autumn 2026)
- **Website**: israir.co.il

**Baggage policy (verified October 2026 on israir.co.il, international flights except New York):**

| Item | Weight / Size | Cost (advance) | Cost (at Ben Gurion) |
|------|---------------|----------------|----------------------|
| Personal item | 40x30x20 cm | Free | Free |
| Carry-on | 10 kg, 55x40x25 cm | $30 per direction | $40 |
| 1st checked bag | 23 kg | $65 per direction | $100 |
| 2nd checked bag | 23 kg | $80 per direction | $120 |
| Bags 3-5 (each) | 23 kg | $120 per direction | $150 |
| Overweight (24-30 kg, first bag only) | -- | +$20 per direction | +$70 |

"Advance" means on the Israir site or personal area up to 6 hours before take-off. Standard fares include no checked bag, **except New York**: there a carry-on and checked bags are included (economy 1 x 23 kg, premium 2 x 23 kg, business 2 x 32 kg). Always confirm the live figure on the Israir baggage-policy page before booking.

### Arkia (IZ)

- **Hub**: Ben Gurion (TLV)
- **Network**: pre-war plans (February 2026) announced about 40 summer destinations; check current routes on arkia.co.il
- **Website**: arkia.co.il

**Baggage**: arkia.co.il blocks automated reading, so this skill carries no Arkia fee table. Read the carry-on and checked-bag allowance and price for the specific route and fare in Arkia's booking flow, and never assume a bag is included or excluded.

### Low-Cost Carriers

**Wizz Air (W6)**: Hungarian low-cost carrier. The February 2026 war forced it to suspend all Israel operations; Wizz resumed TLV on **May 28, 2026** and has kept expanding (in September 2026 it added London Gatwick, Catania, Venice, Cluj and Iasi). Verify the specific route on wizzair.com. Only a personal item (40x30x20 cm) is free on base fares; the 55x40x23 cm trolley needs WIZZ Priority, and checked bags are paid add-ons sold at 10, 20, 26 or 32 kg.

**Ryanair**: Did not restart Tel Aviv for winter 2025-26 (22 routes, about 1 million seats) over a slot and Terminal 1 dispute with Ben Gurion Airport, saying it would return only once those were confirmed. As of October 2026 no return date had been announced.

### Foreign Carriers (snapshot, late October 2026)

Per-airline dates and sources: `references/tlv-carrier-status.md`. Headlines:

- **Flying**: Lufthansa, SWISS, Austrian, Eurowings, Brussels Airlines, ITA, Aegean, Air France, Etihad (Abu Dhabi, now the main Gulf connection), United (Newark, with Chicago and Washington from late October 2026), Delta (New York JFK), British Airways (London, from 25 October 2026), Iberia (Madrid, from 25 October 2026).
- **Suspended**: flydubai (since 30 September 2026, until further notice), Emirates (no TLV service), Turkish Airlines (gave up its Ben Gurion slots in April 2025; check whether it has returned before assuming an Istanbul connection), easyJet (no confirmed date), American (through late March 2027), Air Canada (reports conflict: Toronto from 30 November 2026, or not before end of March 2027). Israeli airlines have not flown to Dubai since February 2026.
- These change weekly: verify the route on the airline's own site before relying on it.

## Seasonal Pricing Guide

### Peak Periods (Most Expensive)

- **Jewish holidays**: Rosh Hashana, Sukkot, Pesach, and Hanukkah (a school break) -- prices climb in the weeks before
- **Summer** (July-August): School vacation, highest demand
- **Christmas and New Year** (late December to early January): Europe's own peak on top of Israeli demand
- **Purim break** (March): Short but expensive window

### Shoulder Seasons (Moderate)

- **April-May** (between Pesach and summer): Good weather, moderate prices
- **September** (between summer and holidays): Brief window before Rosh Hashana
- **Mid-October to early November** (after Sukkot): Prices ease

### Off-Peak (Cheapest)

- **January** (after the New Year return wave): usually the quietest month
- **February** (excluding Purim): Low demand
- **Mid-November to early December** (before Hanukkah): Winter low season

### Upcoming Holiday Dates (Israel)

- **Hanukkah 2026**: from the evening of Friday 4 December to Saturday 12 December 2026. Both ends fall on Shabbat.
- **Purim 2027**: 23 March 2027.
- **Pesach 2027**: from the evening of 21 April to 28 April 2027.

For any other year, take the dates from hebcal.com (Israel schedule) rather than from memory.

## Shabbat-Aware Scheduling

Hebrew-calendar timing constrains flight options in a way generic search tools ignore.

- **El Al does not fly passengers on Shabbat or Jewish holidays.** There is no El Al flight in the air between Friday before sundown and Saturday after nightfall, outbound or return: fly Thursday, Friday early enough to land before Shabbat, or Saturday night onward.
- **Which holidays**: the rest days are Rosh Hashana, Yom Kippur, the first and last days of Sukkot and of Pesach, and Shavuot. Hanukkah, Purim and Chol HaMoed are not rest days, so they do not block flights.
- **Israir and Arkia do fly on Shabbat**: as of May 2026, El Al is the only Israeli airline that does not. Haredi leaders have pressed Israir to stop under a boycott threat, so verify Israir's Shabbat schedule before relying on it.
- **Foreign carriers**: check that the route actually runs on the day you need; many routes are not daily.
- **Observant travelers, any carrier**: ask whether anyone keeps Shabbat or Yom Tov. If so, every flight, including connections, must land before candle-lighting at the arrival point (take the time for that date from hebcal.com), with a margin of several hours for delays and getting home, and not depart before nightfall at the end, whatever the airline.
- **Planning rule**: fix the Shabbat window first. Hanukkah 2026 shows why: on El Al, a trip starting Friday 4 December must leave early enough to land before Shabbat, and a return on Saturday 12 December must wait until after nightfall.

## Entry Requirements and Travel Documents

A cheap fare is worthless if the traveler cannot board or enter, so check documents for **every** passenger before recommending any route. Details and sources: `references/entry-documents.md`; for full visa rules and trip planning abroad use `israeli-abroad-trip-planner`.

| Destination | What an Israeli passport holder needs | Official site |
|-------------|---------------------------------------|---------------|
| Schengen / Europe | Nothing in advance yet: ETIAS is not operating; the EU's last stated target was the last quarter of 2026, but no launch date was announced as of late October 2026 | travel-europe.europa.eu/etias |
| UK | ETA, required since 8 January 2025, for each traveler including babies, also for landside transit | gov.uk/eta |
| USA | ESTA (Visa Waiver Program); an e-Passport is required, and CBP advises applying before buying tickets | esta.cbp.dhs.gov |
| Canada | eTA with a national Israeli passport (a travel document in lieu of passport needs a visa) | canada.ca |
| Any other country, and every transit country | Check that country's official immigration site, and confirm with the airline, before recommending the fare | the country's official site |

Fees change, so read them on the official site; never apply through look-alike sites that charge more.

- **Passport validity**: many countries require at least 6 months beyond the return date. Schengen requires validity 3 months beyond departure from the area AND issue within the last 10 years, so an old passport extended on paper can be refused at boarding. Passports of children under 16 are valid for only 5 years, so check theirs first.
- **Passport timing**: a new biometric passport is issued about 6 weeks after the appointment. Within 48 hours of departure a temporary passport can be issued only at Ben Gurion. ESTA requires an e-Passport, so do not assume a temporary passport qualifies: for a US trip, confirm with the airline or CBP first and plan for the biometric passport.
- **Authorizations follow the passport**: an ESTA or UK ETA is linked to the passport used to apply. A new passport (including a child's renewal) needs a new application before the trip.
- **Dual nationals**: ask which passport each traveler will use. A US citizen, including an Israeli-American, does not apply for ESTA and travels to the US on the US passport; a British citizen does not need a UK ETA. For leaving and entering Israel, check the Population and Immigration Authority's current rule for dual citizens.
- **Names**: book every traveler exactly as the English name line of the passport they will carry; name corrections after booking can be expensive, especially on low-cost carriers and through OTAs.
- **EES** is fully operational since 10 April 2026: Schengen borders record biometrics instead of stamping passports. No advance action is needed.
- **Travel warnings**: before booking a cheap "anywhere" destination, check its National Security Council travel-warning level (gov.il, phone 02-666-7444, 24/7).

## Booking Strategies

### Timing

- **Book several weeks out, not months, and track the price.** Hard "optimal window" claims date fast and rarely beat active price tracking. Around the chagim prices climb in the weeks before the holiday; if the holiday is already close, tell the traveler to book now rather than wait for a dip.
- **Day-of-week effects are small and shift yearly.** Expedia's 2026 data for US domestic flights put Tuesday departures about 14% below Sunday, and named Friday the cheapest day to book; neither is a TLV rule. Do not over-optimize the day, set a price alert instead.
- Set price alerts on Google Flights or KAYAK for routes you're watching, then pounce when the fare dips below the "typical" band on the fare-history graph.

### Money-Saving Tips

1. **Compare across 3+ platforms**: Prices differ significantly between platforms for the same route
2. **Check package deals on Issta**: Flight+hotel bundles can beat booking separately
3. **Use "Everywhere" search on Skyscanner**: Find the cheapest destination for your dates instead of picking a destination first
4. **Consider nearby airports**: For European destinations, flying to a nearby city and taking a train can be cheaper (e.g., fly to Bergamo instead of Milan)
5. **Book baggage in advance**: El Al and Israir charge significantly more for baggage bought at the airport than online in advance
6. **Check Wizz Air for European routes**: Low-cost fares start very low but add-ons (bags, seats) add up -- compare total cost including extras
7. **Flexible dates**: Shifting departure by a day or two can change the fare noticeably; check the date grid or month view
8. **Try multi-city / open-jaw**: For multi-stop Europe trips, flying into one city and out of another (e.g. into Rome, out of Milan) often beats a round-trip. Google Flights and Skyscanner both support multi-city search.
9. **Protect against disruption**: TLV routes still get suspended on short notice. Israeli law gives rights when a flight to or from Israel is cancelled or delayed; for who is liable and how to claim, use `israeli-flight-compensation`. The real money-loss risks are separately ticketed self-transfers (a refund covers only the cancelled segment) and non-refundable hotels, so prefer a single ticket and refundable hotel or insurance that covers airspace closure.
10. **Mind who sells the ticket**: when prices are close, buy from the airline or an Israeli agency rather than an unknown foreign OTA at the top of Skyscanner or KAYAK. In a mass cancellation the seller handles your refund, and Israeli consumer-protection cancellation rules may not reach a foreign seller.

### Flight+Hotel Packages

Israeli agencies (Issta, Lametayel) sell flight+hotel packages that can beat booking separately, especially for Greece, Cyprus, and European city breaks.

### More Booking Levers

Israeli deal sites (e.g. secretflights.co.il), points and miles (El Al Matmid, Israeli cards), and kosher or special meals (request KSML on foreign carriers when booking): see `references/booking-extras.md`.

## How to Search

> **Plan for TLV security.** The Israel Airports Authority advises arriving **3 hours before international departures** (more at holiday peaks). Factor this in when a cheap early-morning fare means a pre-dawn arrival.

**This skill's job is to compare real flights, not to name websites.** Follow the workflow below: build the pre-filled search links for the traveler's exact route and dates, read the live fares off them, add baggage to get a true total, and return an actual comparison. Never substitute remembered or estimated prices for this work (see "Never invent a price").

### Step 1: Gather the Trip

Assume TLV as the origin and ask only for what is missing:

1. Destination (city or airport code, or "anywhere cheap")
2. Dates (specific, or a flexible month)
3. Passengers: adults, each child's age on the travel dates, lap infants under 2, and which passport each traveler will use
4. How many checked bags in total, or carry-on only?
5. Nonstop only, or connections OK?
6. Does anyone keep Shabbat or Yom Tov?
7. Airline preference or budget ceiling (optional)

Fares and baggage differ by age band (infant, child, adult) and a child discount is never guaranteed, so do not compute one yourself: read the price the platform returns for the exact passenger mix.

### Step 2: Build the Pre-Filled Search Links

Construct a real, click-ready search URL for each platform from the route and dates. These URL patterns are taken from the platforms' own result pages; substitute the destination and dates. Skyscanner takes the lowercase airport code (e.g. `ath`, `lca`) and dates as `YYMMDD`; KAYAK takes IATA codes (Rome = `ROM`, Paris = `PAR`, Larnaca = `LCA`) and dates as `YYYY-MM-DD`; Google Flights takes plain city names.

| Platform | Round-trip URL template |
|----------|-------------------------|
| Google Flights | `https://www.google.com/travel/flights?q=Flights+from+TLV+to+{CITY}+on+{YYYY-MM-DD}+returning+{YYYY-MM-DD}&curr=ILS&gl=IL&hl=he` |
| Skyscanner | `https://www.skyscanner.co.il/transport/flights/tlv/{dest}/{YYMMDD}/{YYMMDD}/` |
| KAYAK | `https://il.kayak.com/flights/TLV-{DEST}/{YYYY-MM-DD}/{YYYY-MM-DD}?sort=price_a` |

- **Passengers**: every template opens for 1 adult. Set the full passenger mix on each platform's search form before reading prices; do not guess passenger query parameters.
- **One-way**: drop the second date (Skyscanner: one `YYMMDD` segment; KAYAK: one date).
- **Flexible month** (find the cheapest dates): open the Skyscanner link and switch the date to "Whole month", or use the Google Flights date grid; do not guess a month URL.
- **"Anywhere cheap"**: Skyscanner's "Everywhere" destination or the Google Flights "Explore" map, set on the search form.
- **Nonstop / max-price**: build the base link, then apply the nonstop and price filters on the results page (the sidebar filters), do not guess filter query parameters.
- **Keep one currency**: use `il.kayak.com` (as shown), NOT `www.kayak.com` which defaults to USD. Google Flights `curr=ILS` and Skyscanner `.co.il` are set up for shekels, but confirm the currency each page actually shows. Mixing a USD KAYAK fare into the NIS total in Step 4 is the currency trap in Gotcha 6.
- Worked example (TLV→Athens over Hanukkah, 6-11 Dec 2026): Google Flights `...q=Flights+from+TLV+to+Athens+on+2026-12-06+returning+2026-12-11...`; Skyscanner `.../tlv/ath/261206/261211/`; KAYAK `.../TLV-ATH/2026-12-06/2026-12-11?sort=price_a`.

### Step 3: Pull the Live Fares

Open each link and read the actual results, do not stop at building the URLs:

**Fastest path when a flight-search MCP is connected.** If the Rift flight MCP (formerly Soar, `https://mcp.rift.co`) is available this turn, call `soar_search_flights` (`origin: "TLV"`, `destination`, `date`, `return_date`, and `passengers_detail` with each child's age, or `passengers`) for structured live offers with fare brand and baggage counts, no API key. Binding rules (full detail in `references/soar-mcp-usage.md`):

- **USD only.** Convert with a live rate you read this session (e.g. Bank of Israel, `https://www.boi.org.il/roles/markets/exchangerates/`) and show it, or leave the row in USD. Put the ~3% Israeli card foreign-currency fee inside the ranked total.
- **One source is not a comparison.** It may miss airline-site promotions and Israeli charter seats; say plainly that the result is single-source and never call it "the cheapest available".
- **Use the offer's own baggage counts** in Step 4, not the static tables.
- **Search only.** Never call `soar_book_flight` and never send the traveler to Rift to buy (see Gotcha 9).
- **Rate limit** 5/min, 30/hr per IP, so use the Skyscanner "Whole month" or "Everywhere" options for flexible-month or "anywhere cheap" searches.

- With a browser tool (or a flights MCP), navigate to each URL and read the top 3-5 fares: airline, fare brand (e.g. Lite or Classic), price in shekels, whether the price is per person or for all passengers, number of stops, total duration, and departure/return times.
- **All three platforms render fares with JavaScript**, KAYAK included. Reading live prices needs a real browser/rendering tool or a flights MCP; a plain `WebFetch` returns an empty shell with no fares. If you do NOT have a browser tool this turn, do not report a comparison from `WebFetch` alone, hand the traveler the pre-filled links from Step 2 instead (see "Never invent a price").
- Cross-check at least two platforms; the same route can differ noticeably between Google Flights (airline fares) and Skyscanner (which adds OTA prices).
- For flexible dates, read the cheapest-date cells from the Skyscanner month calendar or the Google Flights date grid.
- For real-time TLV flight status on travel day, the [Ben Gurion Flights](https://agentskills.co.il/en/mcp/ben-gurion-flights) MCP gives live arrivals and departures (it does not return prices).

### Step 4: Normalize to Total Cost

A base fare is not comparable until you add what the traveler actually needs. Rank on the booking total for the whole party:

`total = fare for the whole itinerary + paid extras (carry-on, checked bags beyond the fare's allowance, seats), each per passenger and per direction`.

- **Fare**: if the platform shows a price for all passengers, use it once; if per person, add each passenger's own fare (child fares differ). Count a round-trip fare once, not once per direction.
- **Paid extras are per passenger, per item, per direction.** One Israir first bag at $65 is $130 round trip; a family of four with one bag each pays 4 x $65 x 2 = $520 before conversion. A carry-on is paid on Israir outside New York ($30 per direction) and Wizz (Priority) but included on El Al, so a carry-on-only trip still needs this line.
- **Do not double count**: add only carry-ons and bags beyond what the fare includes (Israir New York, El Al Classic and up).
- **Seats**: a family needs adjacent seats, so on basic fares add a seat fee for every passenger who occupies a seat (not lap infants), each direction.
- **Infants and children**: read each carrier's infant fare and allowance (bag, stroller, car seat) in its booking flow; do not assume either way.
- **Use advance online prices** and say so in the Notes; airport prices are higher.
- **Fees without a table here** (Arkia, Wizz, Aegean, the El Al Lite bag add-on): read the price for that fare brand in the carrier's own booking flow. Aggregators usually surface El Al's cheapest brand, Lite, which has no bag, so check the Classic price on elal.com before claiming El Al wins once bags are added.

**Get everything into one currency first.** The Israir table is in dollars and a Rift fare is in dollars, while the Step 5 table is in NIS. Convert with a rate you read this session, state that rate, and add the ~3% Israeli card conversion fee only to amounts the card is actually charged in foreign currency (if an airline bills shekels, use its shekel amount). Never convert from memory; if you cannot read a rate, show the original currency (Gotcha 8).

El Al includes a checked bag on Classic and up, while Israir (outside New York) and Wizz charge for almost everything. A low base fare on Israir or Wizz routinely loses to El Al Classic once a 23 kg bag is added, this is the single most common comparison mistake.

### Step 5: Present the Comparison

Return a table with the REAL fares you pulled, cheapest total first:

| Option | Airline | Route / Stops | Base (NIS) | Extras (NIS) | Total (NIS) | Source | Notes |
|--------|---------|---------------|-----------|-----------|------------|--------|-------|
| 1 | ... | ... | ... | ... | ... | Google Flights / Skyscanner / Soar (USD) | e.g. no Shabbat return, gate-check carry-on on Lite |

Name the source for every row, and state the conversion rate for any USD-sourced row. If all rows came from one source, say so rather than presenting it as the whole market.

Then give a one-line recommendation covering cheapest total, best value (price vs. stops and timing), and best for a family with bags. Include the Step 2 links so the traveler can book or re-check the live price.

### Never Invent a Price

**Every number in the comparison must come from a page you actually loaded this session.** Do not estimate or fill in "typical" fares from memory; prices change hourly and a fabricated comparison is worse than none. If you cannot read live prices this turn (no browser access, a bot block, or a captcha), write no numbers: hand the traveler the Step 2 links, pre-filled for their route and dates, and say plainly that you could not read the fares yourself.

## Recommended MCP Servers

| MCP | What It Adds |
|-----|-------------|
| [Ben Gurion Flights](https://agentskills.co.il/en/mcp/ben-gurion-flights) | Real-time TLV arrivals and departures from the Israel Airports Authority. Complement the price-comparison workflow with live flight status on travel day. |
| Soar Flight Booking MCP, now Rift (`https://mcp.rift.co`) | Structured live airfare via `soar_search_flights`, no API key needed for search. Use it for prices in Step 3 when you have no browser tool. Prices in USD only. Search tool only: never call its booking tool and never send the traveler there to buy (see Gotcha 9). |

## Gotchas

1. **El Al Lite fares to Europe/UAE have no cabin carry-on**: Lite passengers must send their carry-on to the hold at the gate (free). Only a small personal item fits in the cabin. Lite is not sold on North America routes at all.

2. **Baggage pricing varies wildly between Israeli airlines**: El Al includes bags on Classic and above; Israir charges for everything except a personal item, except on New York flights where bags are included; Arkia's allowance must be read live per route. Always check the specific fare's baggage inclusion before comparing base prices.

3. **Israeli holiday pricing is front-loaded**: Prices climb in the weeks BEFORE the holiday, not on the holiday itself, so a late booking for the holiday period is usually the expensive one.

4. **"Direct" may not mean "nonstop"**: a listing can call a flight with an intermediate stop on the same plane "direct". Check the number of stops on the airline's own site if nonstop matters.

5. **Package and flight-only prices are not comparable**: a package price may include hotel and transfers. Compare a package with a package, and a flight with a flight.

6. **Currency mismatches**: any platform can show another currency if its settings or site version differ (KAYAK's www site, for one). Check the currency on every page before comparing.

7. **Prices must be pulled live, never recalled**: fares change hourly, so a remembered or "typical" number is almost always wrong. Read the current price off the search links every time, and if you cannot, hand over the pre-filled links instead of guessing (see "Never Invent a Price").

8. **Not every number in this skill is already in shekels**: the Israir baggage table above is quoted in dollars, and the Rift (formerly Soar) MCP quotes fares in dollars. The Step 5 table is in NIS. Dropping a `$65` Israir bag into a shekel column as `65` badly understates it and can flip this skill's own conclusion that El Al Classic beats the low-cost carriers once a bag is added. Convert every non-shekel figure using a rate you read this session, state it, and never convert from memory (see Step 4).

9. **The Rift (formerly Soar) MCP is a price source, never a booking venue**: `soar_book_flight` runs sign-in, verification, and payment within one tool. Under Rift's terms Rift is the booking agent, refunds and disputes run through it rather than the airline under Delaware law and binding Delaware arbitration, and buyers appoint it to cancel and rebook their ticket on their own initiative. Israeli consumer-protection cancellation rules may not reach it. See `references/soar-mcp-usage.md`.

10. **A one-adult link prices a family wrong**: the Step 2 links open for one adult. Reading those fares and multiplying by four ignores child fares, lap infants, and per-passenger bags and seats. Set the real passenger mix first and compute the party total per Step 4.

## Bundled Resources

- `references/comparison-platforms.md` -- Detailed platform comparison with URLs and features
- `references/airline-baggage-quick-ref.md` -- Quick-reference baggage table for El Al, Israir and Wizz Air
- `references/soar-mcp-usage.md` -- Rift (formerly Soar) flight-search MCP: tools, parameters, binding constraints
- `references/tlv-carrier-status.md` -- Foreign-carrier status at TLV with dates and sources (October 2026 snapshot)
- `references/entry-documents.md` -- ETIAS, UK ETA, US ESTA, Canada eTA, and Israeli passport timing, with sources
- `references/booking-extras.md` -- Israeli deal sites, points and miles, kosher and special meals

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| El Al hand baggage | https://www.elal.com/eng/baggage/hand-baggage | Carry-on allowance per fare, Lite gate-check rule, Matmid exemption |
| Israir baggage policy | https://www.israir.co.il/Passengers_Info/Baggage_Policy.html | Advance vs airport carry-on and checked-bag pricing, New York inclusions |
| Wizz Air baggage & routes | https://www.wizzair.com/en-gb/help-centre/booking-information-and-services/baggage/baggage-allowance | Base fare inclusions, WIZZ Priority add-on, checked-bag weights |
| ETIAS (official EU) | https://travel-europe.europa.eu/en/etias | Whether ETIAS is operating yet and its announced start date |
| UK ETA (gov.uk) | https://www.gov.uk/eta | ETA requirement and current fee |
| Hebcal (Israel holidays) | https://www.hebcal.com/holidays/ | Holiday and Shabbat dates for the travel year |

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Prices appear in dollars or euros | Site version or currency setting | Use the Step 2 links (`curr=ILS`, `il.kayak.com`, `.co.il`) or switch the currency selector, then confirm the currency shown |
| Aggregator price differs from the airline's site | Different seller, fare brand, or a seller markup | Compare the fare brand and the seller; book with the airline if the price matches |
| Bag fees not shown on the results page | Extras are priced later in the booking flow | Continue to the booking page to read the bag and seat prices before ranking |
