---
name: israeli-abroad-trip-planner
description: "Plans a full trip abroad for Israeli travelers: route, hotels and attractions, anchored by the Israel-specific layer of visa and electronic-authorization rules for an Israeli passport, official Israeli travel warnings, exit restrictions, passport validity and renewal, and travel health and insurance via the kupot. Use when an Israeli is planning or preparing a trip abroad and needs both the itinerary and the Israeli checks. Visa status and travel warnings are always checked live against official sources, never guessed. Do not use for domestic travel in Israel (israeli-travel-planner) or flight price comparison (israeli-flight-finder)."
license: MIT
---

# Israeli Abroad Trip Planner

## Problem
Israelis planning a trip abroad juggle two jobs at once: building a good itinerary (route, hotels, attractions that fit their budget and style) and clearing an Israel-specific gauntlet generic travel tools ignore: does this destination admit an Israeli passport, does it need an electronic authorization before boarding, is there an active travel warning, is anyone under an exit order, is the passport valid long enough, and what about travel health. Global trip planners assume a US or EU passport, so they hand an Israeli traveler advice that is wrong on exactly the parts that get you turned away at the border or denied boarding at check-in. This skill plans the real trip while weaving the Israeli layer in where it matters, and treats the volatile, safety-critical facts (visa and warnings) as things to verify live, not recite.

## Instructions

You are planning a trip abroad for a traveler holding an Israeli passport. Do the itinerary work AND the Israel-specific checks together. Do not railroad: gather what you need, then adapt the order to the traveler.

> [!IMPORTANT]
> Anti-fabrication rule (the core of this skill). Visa requirements for an Israeli passport and Israeli travel warnings change constantly and are safety-critical. NEVER state a country's current visa status or warning level from memory or training data. For every trip, check the CURRENT official source at the time of use. If you cannot verify, say so plainly and defer to the official advisory instead of guessing. Do not build or rely on a stored visa table. Your value here is routing to the right official source, not asserting a status.
>
> The rule covers volatile per-country STATUS. It does not excuse skipping the stable, knowable items in this skill (that an electronic authorization category exists, that exit orders exist, passport lead times, insurance exclusions, medication rules). Those you state.

### Step 1: Gather trip preferences
Collect enough to build a real itinerary:
- Destination(s) and rough dates (or flexibility).
- Party: number of adults, kids and their ages, anyone with mobility or medical needs, anyone on regular prescription medication.
- Budget band and trip style: city break, nature, family, culture, beach, kosher-observant, backpacking, luxury.
- Pace (packed vs relaxed), must-do interests, and any fixed anchors (a wedding, a conference).
- Passport nationality confirmation (Israeli passport assumed; ask about dual citizenship, it cuts both ways, see Step 4).
- Whether anyone in the party is a new oleh within their first years in Israel, or is of draft age. Both change which document they travel on and whether they can leave, see Step 4 and Step 6.

### Step 2: Run the Israel-specific checks EARLY (before locking anything expensive)
These can change or kill a plan, so check them before booking-style commitment.

Use this source-routing table. It maps each question to WHERE to check live. It is deliberately NOT a table of answers.

| Question | Check live at | Notes |
|----------|---------------|-------|
| Does an Israeli passport need a visa here? Visa-free / e-visa / visa / not admitted? | IATA Travel Centre (https://www.iatatravelcentre.com/) selecting Israel as nationality, AND the Foreign Ministry's own visa-exemption table for Israeli passports (https://www.gov.il/BlobFolder/reports/examption_visa-israeli-heb/he/ISR_Visa_Abroad_Heb.pdf), AND the destination's official embassy/consular page for Israeli citizens | Never assume visa-free just because it is visa-free for another nationality. IATA is bot-protected and may show a security check; a human should open it in a browser |
| Visa-free but does it need an ELECTRONIC AUTHORIZATION before boarding? | The destination's own official portal only | See the block below the table. This is a separate question from "do I need a visa" and missing it means denied boarding |
| Is there an Israeli travel warning for this destination? | National Security Council travel warnings (https://www.gov.il/he/departments/dynamiccollectors/travel-warnings-nsc) | The NSC (המל"ל) sets the official warning level. Inquiries line 02-666-7444, answered 24/7 |
| Any consular guidance / recent advisory? | Ministry of Foreign Affairs travel recommendations (https://www.gov.il/he/departments/dynamiccollectors/travel_warnings) | Read alongside the NSC warning |
| Is anyone in the party under an exit order (עיכוב יציאה מהארץ)? | The traveler's personal area on my.gov.il, the Enforcement and Collection Authority (*35592) for a debt-based order, or Population Authority *3450 | Applies to ADULTS, not just minors. See Step 4 |
| Passport-validity rule for entry | Same IATA/embassy pages as the visa check | Many destinations require validity beyond your entry date (a figure often cited is six months); confirm the exact rule per destination, do not assume |
| Transit/layover country rules | IATA Travel Centre for the transit country | A layover can carry its own transit-visa or transit-authorization rule |
| Vaccines / health requirements | Ministry of Health (https://www.gov.il/he/service/vaccination_abroad) and your kupat-cholim travel clinic | Some destinations require proof of vaccination to enter |
| Is anyone's prescription medication restricted at the destination? | The destination's embassy or health/customs authority | See Step 5. Some common Israeli prescriptions are controlled or banned abroad |

> [!IMPORTANT]
> Electronic travel authorizations are a separate gate from visas, and they are where "visa-free" quietly becomes "denied boarding". A growing set of destinations require an approved authorization BEFORE check-in. Israel's own Foreign Ministry says so in its visa table: some countries that exempt Israelis from a visa still require an advance online authorization, usually for a fee, applied for some days before the flight. Two that Israelis hit constantly:
> - **United Kingdom.** Israeli travelers have needed a UK ETA since 8 January 2025, and it covers stays of up to six months. Every traveler needs their own, including babies and children, and one is also needed to transit landside through a UK airport. Apply only at https://www.gov.uk/eta and read the current fee there (it was GBP 20 when this skill was last checked and has been raised more than once, so quote it as "check the portal", not as a fixed price).
> - **United States.** Israel is in the US Visa Waiver Program and Israeli citizens apply through ESTA. Apply only at https://esta.cbp.dhs.gov/. See the passport interactions in Step 4.
>
> Do NOT recite which other countries run such a scheme from memory: this is per-country status and it rots exactly like visa status. Israelis are, for example, currently EXEMPT from Korea's K-ETA for tourism, so a remembered list is worse than no list. For every destination and every transit country, check that country's own official portal. Many paid lookalike sites outrank the real one and charge a markup for nothing. The EU's ETIAS is coming for Schengen but has NO confirmed launch date, so never present its parameters as settled.
>
> **Authorizations are issued against one specific passport.** If anyone renews or replaces a passport after obtaining one (and Step 4 actively encourages renewing early and in the cheap window), re-check before travel that the authorization is still valid for the document they will actually present, and reapply if not. This is a real denied-boarding trap that the skill's own renewal advice can otherwise create.

When you report back, name the source you would check and, if the human has already pulled the live result, work from that. If nothing has been verified yet, tell the traveler these must be confirmed live before booking, and do not fill the gap with a guessed status.

> [!NOTE]
> If you cannot browse. Several pages above (gov.il, IATA, Kol Zchut) block automated access, and some hosts running this skill have no browsing at all. Do not treat that as a dead end and do not guess. Hand the human a precise instruction rather than a bare link: name the page, what to select, and which field to read back (for example: "open the NSC page, find the destination in the country list, and tell me the warning level shown"). Then plan around what they report. Everything in Steps 4 to 7 that is not a per-country status is stable, and you should give it in full regardless, because it is what you can deliver without a live fetch.

### Step 3: Build the itinerary
With the destination cleared enough to proceed, do the normal planning:
- Shape a route/day plan that matches pace and interests.
- Suggest lodging by area and budget band, with reasoning (near transit, family-friendly, near the old town).
- Pick attractions and group them by day to cut backtracking.
- For flights from Israel, note the traveler can compare fares with the `israeli-flight-finder` skill; for live TLV departure/arrival status use the ben-gurion-flights MCP (see below). El Al, Israir and Arkia are the Israeli carriers; most routes run through Ben Gurion (TLV). Treat ROUTE EXISTENCE as volatile, not just the fare: foreign carriers have repeatedly suspended Tel Aviv service on short notice during security escalations and restored it only in phases over months, so for a plan booked far in advance prefer flexible or refundable fares, and check the specific carrier is actually flying the route on your dates. Israeli carriers have tended to keep flying.
- If the itinerary involves renting a car, add an international driving permit to the pre-trip list (Step 7).

### Step 4: Travel documents, exit permission and passport logistics
- The Israeli passport (דרכון) is issued by the Population and Immigration Authority (רשות האוכלוסין וההגירה). Applications are by appointment only, booked online or through *3450, and the passport is issued and passed to the distribution company within six weeks. Build that lead time into the plan rather than saying "renew early" without a number. The fee is reduced from November through the end of February, so a flexible renewal is cheaper in that window.
- Passport validity runs 10 years for age 16 and over. A minor under 16 gets 5 years, so a child's passport can expire while the parents' are still fine; since 18 July 2023 a minor over 16 gets the full 10 years. Check every family member's expiry against the destination's validity rule, not just the adults'.
- Not every Israeli travel document is the full-validity biometric passport book, and visa-waiver schemes can require exactly that. If the US or another waiver destination is on the itinerary, have the traveler check which document they actually hold and confirm it meets that scheme's document requirement, rather than assuming the authorization is a formality.
- Israeli citizens must enter and leave Israel on Israeli travel documentation, even if they also hold a foreign passport.
- **New olim.** An oleh who is three months past aliyah must exit and re-enter Israel on an Israeli travel document. In the first year that document is a תעודת מעבר, valid 5 years. Entitlement to an Israeli passport begins a year after aliyah and depends on actually living in Israel since (broadly, being in the country at least 60% of the time). Do not assume a new oleh is holding a regular Israeli passport, and have them confirm with the destination's consular page which document it will admit.
- **Dual nationality cuts both ways.** A second passport can ease entry to some destinations, but on that state's territory the holder is subject to its laws, including conscription, and Israeli consular protection there is limited. Operationally: carry both, leave and enter Israel on the Israeli document, present the foreign one at the destination if that is the plan, and make sure the passport number given to the airline at booking matches the document actually presented at check-in. Obtaining an EU passport by descent is out of scope here, point them to `israeli-citizenship-by-descent`.
- **Exit orders are not only a children's issue.** A stay-of-exit order (עיכוב יציאה מהארץ) can be issued by a court, a religious court, or a registrar of the Enforcement and Collection Authority (הוצאה לפועל) over a debt, and it stops an ADULT at passport control on the day of the flight. It can also block issuing or renewing a passport. The check is free and fast: the traveler's personal area on my.gov.il, or the Enforcement and Collection Authority on *35592. Cancelling one (https://www.gov.il/he/service/exit_order_cancel_stay) takes time, so check early. For any traveler with an open debt, a divorce file, or unpaid maintenance, raise this rather than waiting to be asked.
- **Minors, two separate consent gates.** Do not conflate them. (1) ISSUING a minor's passport: an application for a child goes through the Population Authority's under-18 route and, where the parents are not married to each other, generally needs both parents' consent. Confirm the exact requirement for the family's situation on the Population Authority passport page, because this is the step that strands separated-parent families late. (2) LEAVING with the minor: because border authorities worldwide have tightened checks on under-18s to prevent abduction, the Foreign Ministry recommends carrying a notarized consent document when a minor travels alone or with only one parent. Rules differ by country, and a family that cleared gate 1 often meets gate 2 at the airline counter. A child under a stay-of-exit order cannot leave without the required consent or a court order.
- Every traveler needs their own passport, including each child; Israel does not add children to a parent's passport.
- **Last-minute departures.** An emergency passport (דרכון חירום, temporary) is valid for one year. Since 1 September 2023 it is issued at 17 Population Authority bureaus as well as at Ben Gurion. Confirm the current appointment and eligibility rules on the gov.il temporary-passport page rather than from a remembered notice; that page carries superseded announcements alongside the current one. Treat the bureau network as the route to plan for and the airport counter as the true last resort; confirm the airport counter's current hours and its departing-soon eligibility before sending anyone there overnight, rather than relying on a remembered opening time. Before recommending it, check the destination will actually accept it: an emergency passport is not the full biometric book, and visa-waiver schemes in particular can require the standard document, so verify admissibility (and whether an existing authorization still applies) rather than assuming the trip proceeds unchanged.
- **If a passport is lost or stolen ABROAD**, the nearest Israeli mission issues a replacement. Be precise about what that is: missions cannot issue a biometric passport, and what they issue is a NON-BIOMETRIC Israeli travel document (passport), not a תעודת מעבר, which is a different instrument. A first travel document requires appearing in person, and where the applicant has been outside Israel more than 10 years they must appear in person AND the document issued is valid one year only. Because it is not the biometric book, it can fail a visa-waiver or authorization requirement on a later leg, so check admissibility for each remaining segment of the route before assuming the trip continues. Tell the traveler to carry a photocopy and a phone scan of the passport, file a local police report, and contact the mission right away, bearing in mind that missions keep their own working days and an in-person appearance may be required, so a weekend loss can cost days before anything can be issued.

### Step 5: Travel health, medication and insurance
- Recommend a travel clinic (מרפאת מטייל) for vaccines and pre-trip advice tuned to age, route, duration and season. The Ministry of Health says to come at least six weeks before departure, because some vaccines are given as a series; Clalit likewise advises booking the first appointment a month and a half before travel. Be accurate about access: travel-clinic entitlement and reimbursement differ by kupah and often by supplementary plan, and the Ministry of Health tells travelers to check what arrangement their own kupah has and what it reimburses BEFORE booking the appointment. Members of any kupah can also use the Ministry of Health district travel clinics or the Mor clinics, so do not leave a Maccabi, Meuhedet or Leumit member without a route.
- **Prescription medication crossing borders.** Some medicines routine in Israel are controlled or banned at the destination, and a few require an advance import permit taking days to weeks. Original labelled packaging, hand luggage, an English doctor's letter, a trip-sized quantity, and the destination's own authority checked for the SPECIFIC drug. Hardest on ADHD stimulants, opioids, benzodiazepines and cannabis products, where the consequence is refusal of entry or confiscation, not a paperwork delay. Full checklist in `references/insurance-and-medication-checklist.md`.
- Be explicit that kupat-cholim coverage abroad is limited. National health insurance delivers the health basket to residents IN Israel; kupah membership is not overseas medical cover, and an overseas medical event runs through the traveler's travel insurer, not the kupah. Treat real overseas cover as travel insurance the traveler must buy.
- Recommend travel insurance (ביטוח נסיעות לחו"ל), as a kupat-cholim add-on or a private policy, and have the traveler verify the lines that actually pay out, not just that a policy exists:
  - Bought BEFORE departure, since many policies cannot be issued or backdated once the traveler has left.
  - The destination is not under an official travel warning, which is commonly an exclusion or a surcharge. The NSC warning from Step 2 therefore has a second consequence: a destination can be legal to fly to and simultaneously uninsurable.
  - Two-wheelers (קטנוע/אופנוע), skiing, diving and trekking, each usually needing its own rider or a motorcycle licence.
  - Medical evacuation and repatriation (פינוי רפואי) and its ceiling, the line that matters most far from a good hospital.
  - Pre-existing conditions and the health declaration (הצהרת בריאות), plus the pregnancy week-cap and age limits.
  - Trip cancellation and interruption, the policy's maximum trip duration, and whether credit-card embedded cover really applies.
  - The assistance company's phone number from the policy, not just the insurer's name. That is the number the traveler calls in an emergency and cannot find at 03:00.

  The full interrogation list, with why each line denies claims, is in `references/insurance-and-medication-checklist.md`. Walk it line by line rather than asking "do you have insurance".
- **Long trips have a National Insurance consequence.** A traveler abroad 18 consecutive months or more who has not paid health insurance contributions for at least 12 months, or who ceases to be a resident, loses entitlement to health services for a waiting period on return of up to six months: one month per year of absence, minimum two and maximum six, where an absence year is any 12 months containing at least 182 days outside Israel, not necessarily consecutive. Raise this for backpacking, sabbatical and extended-stay plans, and point to the National Insurance Institute pages for the calculation and the redemption payment that shortens it.

### Step 6: Timing considerations
- Israeli school holidays drive price and availability: חופש גדול (Jul to Aug), Pesach and Sukkot are peak; flag higher prices and crowding for family trips.
- Peak season squeezes lead times too, not just price. The weeks that make flights expensive are when passport appointments and clinic slots are scarcest, and this skill already asks for six weeks each. Cross the two: a summer trip decided in May needs both booked now.
- Note חגים (holidays) affecting both the traveler's availability and services at the destination.
- If the traveler does מילואים (reserve duty), suggest confirming there is no call-up conflict with the dates before committing.
- If anyone in the party is of draft age (a מלש"ב in the enlistment process, or a soldier in regular service), their military status can constrain travel abroad independently of everything else here. Do not assert what the procedure is; have them confirm the current requirement with their enlistment office (לשכת הגיוס) or unit before dates are locked. On a family summer trip this is the most commonly missed gate: the parents check their own miluim and nobody checks the teenager.

### Step 7: On-the-ground help for Israelis
- **Official emergency channel first.** The Foreign Ministry situation room (מרכז המצב) is staffed 24 hours a day, year-round, for citizens abroad: 02-5303155, WhatsApp 050-507-3969, matzav@mfa.gov.il. Pair it with the mission locator (https://www.gov.il/he/Departments/dynamiccollectors/israeli-consular-services) so the traveler knows which mission covers each stop, and save both to the phone before departure alongside TravIL, the ministry's traveler app.
- For a medical emergency the call order is: local emergency number, then the assistance company named on the travel policy (Step 5), then the mission or situation room. The insurer arranges and pays for treatment and evacuation; the mission cannot.
- A traveler arrested abroad can ask that the Israeli consul be notified, and missions hold lists of local lawyers, which are not recommendations. Israeli missions cannot intervene in another country's legal proceedings.
- Chabad houses (בתי חב"ד) operate worldwide and are a practical anchor for Shabbat meals, kosher food and local help; point to the Chabad center locator to find one near each stop.
- For kosher-observant travelers, plan meals and Shabbat around kosher availability and Chabad locations.
- **Driving.** An international driving permit is required or expected in many countries, must be carried with a valid permanent (plastic) Israeli licence, and is valid three years or until the Israeli licence expires, whichever comes first. It is issued at the Transport Ministry's authorized stations, so arrange it before departure; it cannot be obtained abroad.
- **Entering the Schengen area.** Since 10 April 2026 the EU Entry/Exit System has replaced passport stamping for non-EU travelers, registering facial image and fingerprints and computing stay duration automatically. Allow extra time at first entry, which matters on a tight connection through a European hub, and note the 90-in-180 limit is now machine-enforced, so a traveler with heavy recent EU travel should count days before booking rather than trusting stamps.
- Money and connectivity: an Israeli card with no foreign-exchange fee, a sense of cash-vs-card norms at the destination, and an eSIM or roaming plan chosen by trip length and coverage.

## Examples

### Example 1: Family of four to Greece over חופש גדול, with a 15-year-old and divorced parents
Ten days in early August, two adults and two children (15 and 9), mid-range budget, beaches plus archaeology.

Run Step 2 first and say why: Greece is Schengen, so the entry check, the EES queue at first entry and the 90/180 count all apply, confirmed live rather than from a remembered "Israelis are fine in Europe". Then surface what will actually break this trip. The 15-year-old holds a 5-year minor's passport, so check its expiry against Greece's validity rule now, not in July, and note the six-week issuance plus the August appointment crush. Because the parents are divorced, a renewal generally needs both parents' consent, and separately the Foreign Ministry recommends a notarized consent document if only one parent flies with the children. Check both parents for exit orders. Only then build the itinerary: an Athens base with day trips, one island, ferries booked ahead because August sells out, and lodging quoted at peak prices so the plan is bookable.

### Example 2: Couple to Thailand for three weeks, one partner on daily medication, planning to rent scooters
Beaches and trekking in January, island-hopping by scooter, and a passing mention that one of them takes a regular prescription.

The passing mention is the most important thing said. Check whether that drug is controlled in Thailand and set up the packaging, hand-luggage, English doctor's letter and quantity checklist. The scooter plan is the second trap: standard insurance commonly excludes two-wheelers unless the rider holds a motorcycle licence and buys the extension, so ask before the itinerary assumes scooters. Book the travel clinic at least six weeks out, and check which kupah they are in and what it reimburses. Confirm the entry requirement and any arrival-card or authorization scheme live. Then plan the route, and write the assistance company's number and the situation room number into the final plan.

## Recommended MCP Servers

| MCP Server | URL | What it does |
|-----------|-----|--------------|
| ben-gurion-flights | https://agentskills.co.il/he/mcp/ben-gurion-flights | Real-time flight data from Ben Gurion airport: check a flight's status, search by airline or destination, and track airport activity. It gives live flight status, not booking. |

## Gotchas
- Assuming visa-free because it is visa-free for a US or EU passport. Visa rules are nationality-specific; an Israeli passport can face a different requirement, or be inadmissible, for the same country. Always check with Israel as the nationality.
- Treating "no visa needed" as "nothing to arrange". An electronic authorization is a separate gate the airline checks at boarding, and it catches whole families on the day. Ask it separately, every time, and check the destination's own portal rather than a remembered list of which countries run one.
- Quoting a travel-warning status from memory. Warning levels shift with events; reciting a remembered status is both wrong and dangerous. Pull the live NSC warning every time.
- Treating עיכוב יציאה as a children's problem. A registrar of the Enforcement and Collection Authority can bar an ADULT over a debt, and the traveler finds out at passport control with the family already at the airport. Check every adult early, especially where there is an open debt, maintenance arrears or a divorce file.
- Telling a traveler who lost a passport abroad that they will get a laissez-passer. Missions issue a non-biometric Israeli travel document; תעודת מעבר is a different instrument, and the replacement may not carry the whole remaining route.
- Renewing a passport without re-checking any authorization already issued against the old one, which is a denied-boarding trap the renewal advice itself can create.
- Assuming kupat-cholim covers medical care abroad. It largely does not. Overseas cover is travel insurance the traveler must buy, and a destination under an official warning may be uninsurable even when it is legal to fly to.
- Treating a family's passports as one. Each traveler needs their own, a child's (under 16) is valid only 5 years, and travelling with one parent is a second consent gate on top of the one for issuing the passport.
- Assuming a new oleh holds a regular Israeli passport. In the first year after aliyah the document is a תעודת מעבר, and that is not the same thing at a foreign border.
- Planning over חופש גדול (or Pesach/Sukkot) without noting peak pricing and scarce availability, producing a plan the traveler cannot book at the quoted feel, or whose passport and clinic appointments cannot be obtained in time.

## Reference Links

| Source | URL | What to Check |
|--------|-----|---------------|
| National Security Council travel warnings | https://www.gov.il/he/departments/dynamiccollectors/travel-warnings-nsc | Official warning level for the destination |
| Ministry of Foreign Affairs travel recommendations | https://www.gov.il/he/departments/dynamiccollectors/travel_warnings | Consular guidance and advisories |
| MFA situation room (24/7) | https://www.gov.il/he/pages/matzav | 24/7 emergency channels abroad |
| MFA visa-exemption table for Israeli passports | https://www.gov.il/BlobFolder/reports/examption_visa-israeli-heb/he/ISR_Visa_Abroad_Heb.pdf | Israeli-government visa requirements per destination |
| Leaving Israel with minors | https://www.gov.il/he/pages/leaving_the_country_with_minors | Notarized consent for a minor with one parent |
| Population and Immigration Authority passport service | https://www.gov.il/he/service/application_for_biometric_passport2 | Renewal, appointments, lead time |
| Emergency (temporary) passport | https://www.gov.il/he/pages/temporary_passports | Validity and issuing bureaus |
| Cancelling a stay-of-exit order | https://www.gov.il/he/service/exit_order_cancel_stay | Clearing a debt-based exit order |
| UK electronic travel authorisation | https://www.gov.uk/eta | UK ETA requirement, current fee, official application |
| US ESTA | https://esta.cbp.dhs.gov/ | US authorization for Israeli citizens |
| EU Entry/Exit System | https://home-affairs.ec.europa.eu/policies/schengen/smart-borders/entry-exit-system_en | Biometric entry and 90/180 counting at Schengen |
| IATA Travel Centre | https://www.iatatravelcentre.com/ | Visa, validity and health rules by nationality |
| Ministry of Health vaccinations for travelers | https://www.gov.il/he/service/vaccination_abroad | Vaccine rules and clinic lead time |
| Clalit travel vaccines / travel clinic | https://www.clalit.co.il/he/myrights/vaccines/Pages/travel-vaccines.aspx | Clinic access and vaccine timing |
| National Insurance waiting period after a long stay abroad | https://www.btl.gov.il/Insurance/Living_abroad/Pages/chishuvTkufatHamtana.aspx | Health entitlement lost after a long stay |
| International driving permit stations | https://www.gov.il/he/departments/dynamiccollectors/photo_driving_license_stock | Where to get an IDP and its validity |
| Chabad center locator | https://www.chabad.org/jewish-centers/ | Chabad house near each stop |

## Troubleshooting
- The traveler asks whether a country needs a visa and expects a yes/no. Do not answer from memory. Explain the requirement is nationality-specific and volatile, route them to IATA (Israel selected), the MFA visa table and the destination embassy page, and plan around a live result if one has been pulled. Ask the authorization question separately.
- A gov.il or IATA page will not load or blocks automated access. Common and expected: these sites bot-protect their pages and IATA may show a security check. It is NOT evidence the page is down or the requirement changed. Have the traveler open it in a browser, give them the specific field to read back, and never substitute a guessed status.
- You are running on a host with no browsing. Say so plainly rather than implying you checked. Deliver the full stable layer (passport lead times and validity bands, exit-order check, medication and insurance checklists, emergency numbers) and hand the per-country questions to the human with precise instructions.
- A check comes back negative after booking: visa refused, warning raised, or an exit order surfaces. Do not just report it. Work the salvage: what the cancellation or interruption cover actually pays, whether dates can be moved rather than cancelled, whether the order can be cleared in time, and what a comparable alternative destination looks like at the same budget and dates.
- The traveler wants the cheapest flight or delay compensation. Different job: `israeli-flight-finder` for fares, `israeli-flight-compensation` for delay claims, `israeli-travel-planner` for domestic trips.
- Dates fall in a peak Israeli holiday and the budget will not stretch. Flag the peak explicitly and offer shifting dates or adjusting lodging and route, rather than a plan that reads affordable but is not bookable at that price.

---
This skill is guidance only. Visa rules, entry requirements, electronic-authorization schemes and travel warnings change constantly, so always confirm the current status on the official sources above before you travel. It is not a substitute for official or professional advice.
