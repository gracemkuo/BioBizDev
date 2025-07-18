# service/google_calender_service.py

import json
from datetime import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


def get_credentials():
    """讀取 OAuth 2.0 授權資訊，產生 Google API 憑證"""
    with open("credentials.json") as f:
        creds_data = json.load(f)

    creds = Credentials(
        token=None,
        refresh_token=creds_data["refresh_token"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=creds_data["client_id"],
        client_secret=creds_data["client_secret"],
        scopes=["https://www.googleapis.com/auth/calendar.events"]
    )
    return creds


def create_google_event(summary: str, start_time: datetime, end_time: datetime, email: str) -> str:
    """建立 Google Calendar 活動並邀請對方 email"""
    creds = get_credentials()
    service = build("calendar", "v3", credentials=creds)

    event = {
        "summary": summary,
        "description": "This meeting was auto-scheduled via CRM system.",
        "start": {
            "dateTime": start_time.isoformat(),
            "timeZone": "Asia/Dubai",  # 請根據你所在區域更換
        },
        "end": {
            "dateTime": end_time.isoformat(),
            "timeZone": "Asia/Dubai",
        },
        "attendees": [
            {"email": email}
        ],
        "reminders": {
            "useDefault": True
        }
    }

    created_event = service.events().insert(calendarId="primary", body=event, sendUpdates="all").execute()
    return created_event.get("htmlLink")
