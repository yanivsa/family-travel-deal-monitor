import argparse
import base64
import json
import os
from email.message import EmailMessage
from pathlib import Path
from urllib import parse, request

TOKEN_URL = "https://oauth2.googleapis.com/token"
GMAIL_SEND_URL = "https://gmail.googleapis.com/gmail/v1/users/me/messages/send"
DEFAULT_ALERT_SUBJECT = "🚨 Sukkot 30%+ Price Drop"
TEST_SUBJECT = "✅ Family Travel Monitor Gmail OAuth2 TEST"


def build_message(sender: str, recipient: str, subject: str, body: str) -> EmailMessage:
    message = EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)
    return message


def load_credentials():
    client_id = os.getenv("GMAIL_OAUTH_CLIENT_ID", "").strip()
    client_secret = os.getenv("GMAIL_OAUTH_CLIENT_SECRET", "").strip()
    refresh_token = os.getenv("GMAIL_OAUTH_REFRESH_TOKEN", "").strip()
    sender = os.getenv("GMAIL_SENDER", "").strip()
    recipient = os.getenv("ALERT_EMAIL_TO", "").strip() or sender

    missing = []
    if not client_id:
        missing.append("GMAIL_OAUTH_CLIENT_ID")
    if not client_secret:
        missing.append("GMAIL_OAUTH_CLIENT_SECRET")
    if not refresh_token:
        missing.append("GMAIL_OAUTH_REFRESH_TOKEN")
    if not sender:
        missing.append("GMAIL_SENDER")
    if missing:
        raise RuntimeError("missing Gmail OAuth2 configuration: " + ", ".join(missing))
    if not recipient:
        raise RuntimeError("alert recipient is missing")
    return client_id, client_secret, refresh_token, sender, recipient


def refresh_access_token(client_id: str, client_secret: str, refresh_token: str) -> str:
    payload = parse.urlencode(
        {
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh_token,
            "grant_type": "refresh_token",
        }
    ).encode("utf-8")
    req = request.Request(
        TOKEN_URL,
        data=payload,
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        with request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        raise RuntimeError(f"Gmail OAuth2 token refresh failed: {exc}") from exc
    token = str(data.get("access_token") or "").strip()
    if not token:
        raise RuntimeError("Gmail OAuth2 token refresh returned no access_token")
    return token


def encode_raw_message(message: EmailMessage) -> str:
    return base64.urlsafe_b64encode(message.as_bytes()).decode("ascii").rstrip("=")


def send_message(message: EmailMessage, access_token: str) -> str:
    body = json.dumps({"raw": encode_raw_message(message)}).encode("utf-8")
    req = request.Request(
        GMAIL_SEND_URL,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
    )
    try:
        with request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
    except Exception as exc:
        raise RuntimeError(f"Gmail API send failed: {exc}") from exc
    message_id = str(data.get("id") or "").strip()
    if not message_id:
        raise RuntimeError("Gmail API send returned no message id")
    return message_id


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--alert", default="travel/alert.md")
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()

    client_id, client_secret, refresh_token, sender, recipient = load_credentials()

    if args.test:
        subject = TEST_SUBJECT
        body = (
            "Family Travel Deal Monitor Gmail OAuth2 delivery test succeeded.\n\n"
            "Production alerts are sent only for a verified 30%+ drop in flight, hotel, "
            "or total vacation price.\n"
        )
    else:
        alert_path = Path(args.alert)
        if not alert_path.exists():
            print("No alert file; no email required")
            return 0
        subject = DEFAULT_ALERT_SUBJECT
        body = alert_path.read_text(encoding="utf-8")

    access_token = refresh_access_token(client_id, client_secret, refresh_token)
    message = build_message(sender, recipient, subject, body)
    message_id = send_message(message, access_token)
    print(f"Gmail OAuth2 alert delivered successfully (message_id={message_id})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
