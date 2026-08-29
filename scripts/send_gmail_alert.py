import argparse
import os
import smtplib
import ssl
from email.message import EmailMessage
from pathlib import Path

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465
DEFAULT_ALERT_SUBJECT = "🚨 Sukkot 30%+ Price Drop"
TEST_SUBJECT = "✅ Family Travel Monitor email TEST"


def build_message(sender: str, recipient: str, subject: str, body: str) -> EmailMessage:
    message = EmailMessage()
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)
    return message


def send_message(message: EmailMessage, username: str, app_password: str) -> None:
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, context=context, timeout=30) as smtp:
        smtp.login(username, app_password)
        smtp.send_message(message)


def load_credentials():
    username = os.getenv("GMAIL_USERNAME", "").strip()
    app_password = os.getenv("GMAIL_APP_PASSWORD", "").strip()
    recipient = os.getenv("ALERT_EMAIL_TO", "").strip() or username
    if not username:
        raise RuntimeError("GMAIL_USERNAME secret is missing")
    if not app_password:
        raise RuntimeError("GMAIL_APP_PASSWORD secret is missing")
    if not recipient:
        raise RuntimeError("alert recipient is missing")
    return username, app_password, recipient


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--alert", default="travel/alert.md")
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()

    username, app_password, recipient = load_credentials()

    if args.test:
        subject = TEST_SUBJECT
        body = (
            "Family Travel Deal Monitor Gmail delivery test succeeded.\n\n"
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

    message = build_message(username, recipient, subject, body)
    send_message(message, username, app_password)
    print("Gmail alert delivered successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
