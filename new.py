import re

INPUT_ICS = "Final Events - Subevents Calendar.ics"

OUTPUT_ICS = "reelongo_CLONE_MINIMAL.ics"

CATEGORY_KEYWORDS = [
    "Wedding", "Birthday", "Haldi", "Reception",
    "Engagement", "Brand Shoot", "Decor"
]

def extract_category(summary):
    for k in CATEGORY_KEYWORDS:
        if k.lower() in summary.lower():
            return k
    return "General"

def extract_context(summary):
    match = re.search(r"(ROGL\d+)", summary)
    return match.group(1) if match else "NA"

def extract_creator(summary):
    if "|" in summary:
        tail = summary.split("|")[-1].strip()
        if re.fullmatch(r"C\d+", tail):
            return tail
    return "UNASSIGNED"

def normalize_summary(original):
    category = extract_category(original)
    context = extract_context(original)
    creator = extract_creator(original)
    return f"{category} – {context} | {creator}"

with open(INPUT_ICS, "r", encoding="utf-8") as fin:
    lines = fin.readlines()

out_lines = []
inside_event = False

for line in lines:
    stripped = line.strip()

    if stripped == "BEGIN:VEVENT":
        inside_event = True
        out_lines.append(line)
        continue

    if stripped == "END:VEVENT":
        inside_event = False
        out_lines.append(line)
        continue

    if inside_event and stripped.startswith("SUMMARY:"):
        original_summary = stripped[len("SUMMARY:"):].strip()
        new_summary = normalize_summary(original_summary)
        out_lines.append(f"SUMMARY:{new_summary}\n")
        continue

    # EVERYTHING else stays byte-for-byte
    out_lines.append(line)

with open(OUTPUT_ICS, "w", encoding="utf-8") as fout:
    fout.writelines(out_lines)

print(f"✅ Minimal-clone calendar created: {OUTPUT_ICS}")

from icalendar import Calendar, Event
from datetime import datetime
import pytz
import re

INPUT_FILE = "Final Events - Subevents Calendar.ics"
OUTPUT_FILE = "Final Events - Subevents Calendar (System).ics"

IST = pytz.timezone("Asia/Kolkata")

CATEGORY_KEYWORDS = {
    "WEDDING": ["wedding", "haldi", "engagement", "reception", "pellikoduku", "pellikuthuru"],
    "BIRTHDAY": ["birthday", "bday"],
    "BABY": ["baby", "babyshower", "annaprasannam"],
    "BRAND": ["shoot", "promo", "launch", "brand"],
    "CORPORATE": ["conference", "meeting", "auction"],
}

def infer_category(text):
    text = text.lower()
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(k in text for k in keywords):
            return category
    return "OTHER"

def extract(pattern, text):
    match = re.search(pattern, text)
    return match.group(0) if match else "UNKNOWN"

with open(INPUT_FILE, "rb") as f:
    original_cal = Calendar.from_ical(f.read())

system_cal = Calendar()
system_cal.update(original_cal)

for component in original_cal.walk():
    if component.name != "VEVENT":
        continue

    new_event = Event()
    new_event.update(component)

    summary = str(component.get("SUMMARY", ""))
    description = str(component.get("DESCRIPTION", ""))

    category = infer_category(summary + " " + description)
    lead_code = extract(r"ROGL\d+", summary + description)
    sub_event_id = extract(r"(ROGL\d+-E\d+-S\d+)", summary + description)

    assigned = "YES" if "@" in description else "NO"
    crew_count = "2" if assigned == "YES" else "0"

    system_metadata = f"""
--- SYSTEM METADATA ---
CATEGORY: {category}
ASSIGNED: {assigned}
CREW_COUNT: {crew_count}
LEAD_CODE: {lead_code}
SUB_EVENT_ID: {sub_event_id}
SYSTEM_VERSION: v1.0
LAST_SYNCED: {datetime.now(IST).isoformat()}
"""

    new_event["DESCRIPTION"] = description + system_metadata

    system_cal.add_component(new_event)

with open(OUTPUT_FILE, "wb") as f:
    f.write(system_cal.to_ical())

print("✅ System calendar generated successfully.")

