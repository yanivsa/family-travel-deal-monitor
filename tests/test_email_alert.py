import json
from unittest.mock import patch

from scripts import send_gmail_alert


def test_build_message_uses_sender_recipient_subject_and_body():
    message = send_gmail_alert.build_message(
        "sender@example.com",
        "recipient@example.com",
        "Subject",
        "Body",
    )
    assert message["From"] == "sender@example.com"
    assert message["To"] == "recipient@example.com"
    assert message["Subject"] == "Subject"
    assert "Body" in message.get_content()


def test_load_credentials_requires_oauth_and_uses_sender_as_recipient(monkeypatch):
    monkeypatch.setenv("GMAIL_OAUTH_CLIENT_ID", "client-id")
    monkeypatch.setenv("GMAIL_OAUTH_CLIENT_SECRET", "client-secret")
    monkeypatch.setenv("GMAIL_OAUTH_REFRESH_TOKEN", "refresh-token")
    monkeypatch.setenv("GMAIL_SENDER", "sender@example.com")
    monkeypatch.delenv("ALERT_EMAIL_TO", raising=False)
    values = send_gmail_alert.load_credentials()
    assert values == (
        "client-id",
        "client-secret",
        "refresh-token",
        "sender@example.com",
        "sender@example.com",
    )


def test_load_credentials_rejects_missing_refresh_token(monkeypatch):
    monkeypatch.setenv("GMAIL_OAUTH_CLIENT_ID", "client-id")
    monkeypatch.setenv("GMAIL_OAUTH_CLIENT_SECRET", "client-secret")
    monkeypatch.delenv("GMAIL_OAUTH_REFRESH_TOKEN", raising=False)
    monkeypatch.setenv("GMAIL_SENDER", "sender@example.com")
    try:
        send_gmail_alert.load_credentials()
    except RuntimeError as exc:
        assert "GMAIL_OAUTH_REFRESH_TOKEN" in str(exc)
    else:
        raise AssertionError("missing refresh token should fail")


def test_refresh_access_token_uses_refresh_grant():
    response = patch("scripts.send_gmail_alert.request.urlopen")
    with response as urlopen:
        cm = urlopen.return_value.__enter__.return_value
        cm.read.return_value = json.dumps({"access_token": "access-123"}).encode()
        token = send_gmail_alert.refresh_access_token("cid", "secret", "refresh")
        assert token == "access-123"
        req = urlopen.call_args.args[0]
        body = req.data.decode("utf-8")
        assert "grant_type=refresh_token" in body
        assert "refresh_token=refresh" in body


def test_send_message_calls_gmail_api_with_bearer_token():
    message = send_gmail_alert.build_message(
        "sender@example.com",
        "recipient@example.com",
        "Subject",
        "Body",
    )
    with patch("scripts.send_gmail_alert.request.urlopen") as urlopen:
        cm = urlopen.return_value.__enter__.return_value
        cm.read.return_value = json.dumps({"id": "gmail-message-id"}).encode()
        message_id = send_gmail_alert.send_message(message, "access-123")
        assert message_id == "gmail-message-id"
        req = urlopen.call_args.args[0]
        assert req.full_url == send_gmail_alert.GMAIL_SEND_URL
        assert req.headers["Authorization"] == "Bearer access-123"
        payload = json.loads(req.data.decode("utf-8"))
        assert payload["raw"]
