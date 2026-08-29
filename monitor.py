import json, os, sys, urllib.request
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "travel" / "data.json"
HISTORY = ROOT / "travel" / "history.jsonl"
ALERT = ROOT / "travel" / "alert.md"
TZ = ZoneInfo("Asia/Jerusalem")
ALLOWED_DATES = {("2026-09-27","2026-10-01"),("2026-09-27","2026-10-02"),("2026-09-28","2026-10-01"),("2026-09-28","2026-10-02")}
EXCLUDED = {"turkey","türkiye","egypt","jordan","uae","united arab emirates","bahrain","qatar","oman","saudi arabia","morocco","tunisia","algeria","lebanon","syria","iraq","yemen","kuwait","libya"}
CATEGORIES = ["BEST VALUE","BEST PRICE","SMART UPGRADE / SURPRISE"]

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def validate(payload):
    deals = payload.get("deals", [])
    if len(deals) != 3:
        raise ValueError("provider payload must contain exactly 3 deals")
    if [d.get("category") for d in deals] != CATEGORIES:
        raise ValueError("categories/order do not match output contract")
    for d in deals:
        dep = d.get("departure_date")
        ret = d.get("return_date")
        if dep and ret and (dep, ret) not in ALLOWED_DATES:
            raise ValueError(f"out-of-window deal: {dep} -> {ret}")
        if ret == "2026-10-02" and d.get("return_morning") is not True:
            raise ValueError("2026-10-02 return must be explicitly morning")
        text = " ".join(str(d.get(k,"")) for k in ("destination","country","hotel")).lower()
        if any(x in text for x in EXCLUDED):
            raise ValueError(f"excluded destination: {d.get('destination')}")
        if not d.get("verified", True):
            raise ValueError("unverified deal cannot replace last-known-good Top 3")
        if not isinstance(d.get("total_ils"), (int,float)) or d["total_ils"] <= 0:
            raise ValueError("invalid total_ils")
        if not d.get("flight_url") or not d.get("hotel_url"):
            raise ValueError("reproducible flight_url and hotel_url are required")
    return payload

def fetch_provider(url):
    req = urllib.request.Request(url, headers={"User-Agent":"family-travel-deal-monitor/1.0"})
    with urllib.request.urlopen(req, timeout=45) as r:
        return json.load(r)

def meaningful(old, new):
    old_by = {d["category"]: d for d in old.get("deals", [])}
    changes = []
    for nd in new.get("deals", []):
        od = old_by.get(nd["category"])
        if not od:
            changes.append(f"NEW {nd['category']}: {nd.get('destination')}")
            continue
        if nd.get("destination") != od.get("destination"):
            changes.append(f"{nd['category']} changed: {od.get('destination')} → {nd.get('destination')}")
        op, np = float(od.get("total_ils",0)), float(nd.get("total_ils",0))
        if op > 0:
            delta = np-op
            pct = delta/op*100
            if abs(delta) >= 300 or abs(pct) >= 4:
                changes.append(f"{nd['category']} {nd.get('destination')}: ₪{delta:+,.0f} ({pct:+.1f}%)")
        if abs(float(nd.get("effective_vacation_hours_num",0))-float(od.get("effective_vacation_hours_num",0))) >= 6:
            changes.append(f"{nd['category']} time value changed materially")
    return changes

def main():
    current = load(DATA)
    url = os.getenv("TRAVEL_PROVIDER_JSON_URL", "").strip()
    if not url:
        print("No authorized live provider endpoint configured; preserving last-known-good data.")
        ALERT.unlink(missing_ok=True)
        return 0
    try:
        incoming = validate(fetch_provider(url))
    except Exception as e:
        print(f"Provider failed validation/access: {e}; preserving last-known-good data.", file=sys.stderr)
        ALERT.unlink(missing_ok=True)
        return 0
    incoming["checked_at"] = datetime.now(TZ).strftime("%Y-%m-%d %H:%M Asia/Jerusalem")
    changes = meaningful(current, incoming)
    DATA.write_text(json.dumps(incoming, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    HISTORY.parent.mkdir(parents=True, exist_ok=True)
    with HISTORY.open("a", encoding="utf-8") as f:
        f.write(json.dumps({"checked_at":incoming["checked_at"],"deals":[{"category":d["category"],"destination":d.get("destination"),"total_ils":d.get("total_ils"),"family_value":d.get("family_value")} for d in incoming["deals"]]}, ensure_ascii=False)+"\n")
    if changes:
        body = "# Travel deal monitor — meaningful change\n\n" + "\n".join(f"- {x}" for x in changes) + "\n\nDashboard: https://yanivsa.github.io/family-travel-deal-monitor/\n"
        ALERT.write_text(body, encoding="utf-8")
    else:
        ALERT.unlink(missing_ok=True)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
