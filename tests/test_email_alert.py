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


def test_send_message_logs_in_and_sends():
    message = send_gmail_alert.build_message(
        "sender@example.com",
        "recipient@example.com",
        "Subject",
        "Body",
    )
    with patch("scripts.send_gmail_alert.smtplib.SMTP_SSL") as smtp_cls:
        smtp = smtp_cls.return_value.__enter__.return_value
        send_gmail_alert.send_message(message, "sender@example.com", "app-password")
        smtp.login.assert_called_once_with("sender@example.com", "app-password")
        smtp.send_message.assert_called_once_with(message)


def test_load_credentials_uses_sender_as_recipient_by_default(monkeypatch):
    monkeypatch.setenv("GMAIL_USERNAME", "sender@example.com")
    monkeypatch.setenv("GMAIL_APP_PASSWORD", "secret")
    monkeypatch.delenv("ALERT_EMAIL_TO", raising=False)
    username, password, recipient = send_gmail_alert.load_credentials()
    assert username == "sender@example.com"
    assert password == "secret"
    assert recipient == "sender@example.com"


def test_load_credentials_rejects_missing_app_password(monkeypatch):
    monkeypatch.setenv("GMAIL_USERNAME", "sender@example.com")
    monkeypatch.delenv("GMAIL_APP_PASSWORD", raising=False)
    try:
        send_gmail_alert.load_credentials()
    except RuntimeError as exc:
        assert "GMAIL_APP_PASSWORD" in str(exc)
    else:
        raise AssertionError("missing app password should fail")
