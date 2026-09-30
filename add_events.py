from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]
SERVICE_ACCOUNT_FILE = "service_account.json"

CALENDAR_ID = "69bca44b6439bfc3406bed4a7930754e85e50940efb9804438bb39b4fd3dbdaf@group.calendar.google.com"

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

service = build("calendar", "v3", credentials=credentials)

events = [
    {
        "summary": "Wedding – Sisir | C9",
        "start": {
            "dateTime": "2026-02-22T10:00:00+05:30",
            "timeZone": "Asia/Kolkata"
        },
        "end": {
            "dateTime": "2026-02-22T14:00:00+05:30",
            "timeZone": "Asia/Kolkata"
        },
        "colorId": "10"  # green
    },
    {
        "summary": "Birthday – Tapswini | C6",
        "start": {
            "dateTime": "2026-02-22T12:30:00+05:30",
            "timeZone": "Asia/Kolkata"
        },
        "end": {
            "dateTime": "2026-02-22T15:30:00+05:30",
            "timeZone": "Asia/Kolkata"
        },
        "colorId": "5"  # yellow
    },
    {
        "summary": "Engagement – Greeshma | C4",
        "start": {
            "dateTime": "2026-02-22T13:00:00+05:30",
            "timeZone": "Asia/Kolkata"
        },
        "end": {
            "dateTime": "2026-02-22T17:00:00+05:30",
            "timeZone": "Asia/Kolkata"
        },
        "colorId": "11"  # red
    }
]

for event in events:
    service.events().insert(
        calendarId=CALENDAR_ID,
        body=event
    ).execute()

print("Dummy events added successfully!")
