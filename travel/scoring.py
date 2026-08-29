"""
Scoring and Effective Vacation Time module for Family Travel Deal Monitor.
Calculates EVT, Time Value ("מצוין", "טוב", "סביר"), and Family Value (0-100).
Family composition: 2 adults + 3 children (ages 10, 7, 2).
"""

from datetime import datetime, time, timedelta

def parse_time(t_str: str) -> time:
    """Parse time string like '06:20' or '13:00'."""
    try:
        t_str = t_str.strip().split("→")[0].strip()
        parts = t_str.split(":")
        return time(hour=int(parts[0]), minute=int(parts[1]))
    except Exception:
        return time(12, 0)

def calculate_evt_hours(departure_date: str, return_date: str, outbound_str: str, return_str: str) -> int:
    """
    Calculates Effective Vacation Time in net hours available at destination.
    Assumes arrival at destination approx 1.5 - 2 hrs after departure (or flight length) and departure back ~3 hrs before return flight.
    """
    try:
        dep_dt = datetime.strptime(departure_date, "%Y-%m-%d")
        ret_dt = datetime.strptime(return_date, "%Y-%m-%d")

        out_parts = outbound_str.split("→") if "→" in outbound_str else [outbound_str, outbound_str]
        ret_parts = return_str.split("→") if "→" in return_str else [return_str, return_str]

        # Flight departure time (TLV local)
        out_dep_t = parse_time(out_parts[0])
        # Arrival at destination
        out_arr_t = parse_time(out_parts[1]) if len(out_parts) > 1 else time((out_dep_t.hour + 2) % 24, out_dep_t.minute)

        # Return flight departure time (Dest local)
        ret_dep_t = parse_time(ret_parts[0])

        start_vacation = datetime.combine(dep_dt.date(), out_arr_t) + timedelta(hours=1) # 1 hr post-landing check-out/transfer
        end_vacation = datetime.combine(ret_dt.date(), ret_dep_t) - timedelta(hours=2.5) # 2.5 hrs pre-flight transfer/check-in

        diff = (end_vacation - start_vacation).total_seconds() / 3600.0
        return max(0, int(round(diff)))
    except Exception:
        # Fallback estimation based on days
        days = 4 if departure_date.endswith("27") and return_date.endswith("02") else (3 if departure_date.endswith("28") and return_date.endswith("01") else 4)
        return days * 22

def get_time_value(evt_hours: int) -> str:
    """
    Time Value categorization:
    >= 85 hrs: "מצוין"
    65-84 hrs: "טוב"
    < 65 hrs: "סביר"
    """
    if evt_hours >= 85:
        return "מצוין"
    elif evt_hours >= 65:
        return "טוב"
    else:
        return "סביר"

def calculate_family_value(deal: dict) -> int:
    """
    Calculate Family Value Score (0-100) for 2 adults + 3 children (10, 7, 2).
    Evaluates total price (ILS), EVT hours, hotel stars/score, direct flight, room config/family suitability.
    """
    total_ils = deal.get("total_ils", 10000)
    evt_hours = deal.get("effective_vacation_hours") or calculate_evt_hours(
        deal.get("departure_date", "2026-09-28"),
        deal.get("return_date", "2026-10-01"),
        deal.get("outbound", "10:00 → 12:00"),
        deal.get("return", "10:00 → 12:00")
    )

    hotel_stars = deal.get("stars", 4)
    guest_score = deal.get("guest_score", 8.0)
    is_direct = deal.get("direct", True)
    benefits = deal.get("family_benefits", [])

    # 1. Price score component (0 - 40 pts) - Target baseline ~ 8000 ILS
    # 7000 ILS => 40 pts, 12000 ILS => 15 pts
    price_pts = max(5, min(40, 40 - (total_ils - 7000) / 250))

    # 2. EVT component (0 - 25 pts)
    # 95 hrs => 25 pts, 60 hrs => 10 pts
    evt_pts = max(5, min(25, (evt_hours - 40) * 0.4))

    # 3. Hotel quality component (0 - 20 pts)
    # stars (max 8) + guest_score (max 12)
    hotel_pts = (hotel_stars / 5.0 * 8.0) + (guest_score / 10.0 * 12.0)

    # 4. Family convenience & benefits (0 - 15 pts)
    direct_pts = 5 if is_direct else 0
    benefit_pts = min(10, len(benefits) * 3)
    family_pts = direct_pts + benefit_pts

    score = int(round(price_pts + evt_pts + hotel_pts + family_pts))
    return max(50, min(100, score))
