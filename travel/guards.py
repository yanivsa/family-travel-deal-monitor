"""
Guards and validation logic for Family Travel Deal Monitor.
Constraints:
- Dates only: 2026-09-27 or 2026-09-28 outbound; 2026-10-01 or 2026-10-02 morning return.
- Exclude Turkey and Arab countries.
"""

ALLOWED_DATES = {
    ("2026-09-27", "2026-10-01"),
    ("2026-09-27", "2026-10-02"),
    ("2026-09-28", "2026-10-01"),
    ("2026-09-28", "2026-10-02")
}

EXCLUDED_DESTINATIONS = {
    "turkey", "türkiye", "egypt", "jordan", "uae", "united arab emirates",
    "bahrain", "qatar", "oman", "saudi arabia", "morocco", "tunisia",
    "algeria", "lebanon", "syria", "iraq", "yemen", "kuwait", "libya"
}

def is_allowed_date_pair(dep_date: str, ret_date: str) -> bool:
    return (dep_date, ret_date) in ALLOWED_DATES

def is_morning_return(ret_date: str, return_time: str = None, return_morning_flag: bool = None) -> bool:
    if ret_date != "2026-10-02":
        return True
    if return_morning_flag is True:
        return True
    if return_time:
        # Check hour < 12:00
        time_part = return_time.strip().split("→")[0].strip() if "→" in return_time else return_time.strip()
        try:
            hour = int(time_part.split(":")[0])
            return hour < 12
        except (ValueError, IndexError):
            pass
    return False

def is_destination_excluded(text: str) -> bool:
    if not text:
        return False
    norm = text.lower()
    return any(excluded in norm for excluded in EXCLUDED_DESTINATIONS)

def validate_deal_guards(deal: dict) -> tuple[bool, str]:
    dep = deal.get("departure_date") or deal.get("dates", "").split("–")[0]
    ret = deal.get("return_date")

    # Parse dates if needed
    if (not dep or not ret) and deal.get("dates"):
        # e.g., "28.9–2.10" or "27.9–1.10"
        parts = deal.get("dates").split("–")
        if len(parts) == 2:
            d_p, r_p = parts[0].strip(), parts[1].strip()
            dep = f"2026-09-{int(d_p.split('.')[0]):02d}"
            ret = f"2026-10-{int(r_p.split('.')[0]):02d}"

    if dep and ret and not is_allowed_date_pair(dep, ret):
        return False, f"Date pair ({dep}, {ret}) is not in allowed combinations."

    ret_time = deal.get("return", "")
    return_morning_flag = deal.get("return_morning")
    if ret == "2026-10-02" and not is_morning_return(ret, ret_time, return_morning_flag):
        return False, "Return on 2026-10-02 must be morning return."

    loc_text = " ".join(str(deal.get(k, "")) for k in ("destination", "country", "hotel", "airport"))
    if is_destination_excluded(loc_text):
        return False, f"Destination or country in '{loc_text}' is excluded."

    return True, "OK"
