# Gmail OAuth2 setup for GitHub Actions

Production email alerts use the Gmail API with OAuth2 and the single scope:

`https://www.googleapis.com/auth/gmail.send`

No Google account password or Gmail App Password is stored in GitHub.

## One-time Google setup

1. Create or select a Google Cloud project.
2. Enable the Gmail API.
3. Configure Google Auth Platform / OAuth consent for the Gmail account that will send alerts.
4. Create an OAuth Client ID of type **Desktop app**.
5. Run locally:

```bash
python scripts/gmail_oauth_bootstrap.py \
  --client-id '<CLIENT_ID>' \
  --client-secret '<CLIENT_SECRET>'
```

6. Sign in to Google in the browser and grant only Gmail send permission.
7. The helper prints a refresh token. Do not commit or share it.

## GitHub Actions secrets

Add these repository Actions secrets:

- `GMAIL_OAUTH_CLIENT_ID`
- `GMAIL_OAUTH_CLIENT_SECRET`
- `GMAIL_OAUTH_REFRESH_TOKEN`
- `GMAIL_SENDER` — the Gmail address authorized in Google
- `ALERT_EMAIL_TO` — optional; defaults to `GMAIL_SENDER`

The old `GMAIL_USERNAME` and `GMAIL_APP_PASSWORD` secrets are not used.

## Acceptance test

Run **Process Family Travel Provider Feed** manually with `email_test=true`.
The workflow must fail if OAuth2 is missing/invalid and succeed only after Gmail returns a real message id.

Production alerts are sent only when `travel/alert.md` exists for a verified 30%+ price drop.
