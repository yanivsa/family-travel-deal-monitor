"""One-time local helper to authorize Gmail send-only access.

Usage:
  python scripts/gmail_oauth_bootstrap.py --client-id ... --client-secret ...

The script opens a localhost OAuth callback, prints the Google authorization URL,
and exchanges the returned code for a refresh token. Do not commit the token.
"""

import argparse
import json
import secrets
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse, request

AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
SCOPE = "https://www.googleapis.com/auth/gmail.send"


class CallbackHandler(BaseHTTPRequestHandler):
    result = {}
    expected_state = ""

    def do_GET(self):
        params = parse.parse_qs(parse.urlparse(self.path).query)
        state = (params.get("state") or [""])[0]
        code = (params.get("code") or [""])[0]
        error = (params.get("error") or [""])[0]
        if state != self.expected_state:
            error = "state_mismatch"
        self.__class__.result = {"code": code, "error": error}
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        if error:
            self.wfile.write(f"Authorization failed: {error}. You can close this tab.".encode())
        else:
            self.wfile.write(b"Gmail authorization received. You can close this tab and return to the terminal.")

    def log_message(self, format, *args):
        return


def exchange_code(client_id, client_secret, code, redirect_uri):
    payload = parse.urlencode(
        {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
        }
    ).encode("utf-8")
    req = request.Request(
        TOKEN_URL,
        data=payload,
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with request.urlopen(req, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--client-id", required=True)
    parser.add_argument("--client-secret", required=True)
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args()

    redirect_uri = f"http://127.0.0.1:{args.port}/"
    state = secrets.token_urlsafe(24)
    CallbackHandler.expected_state = state
    server = HTTPServer(("127.0.0.1", args.port), CallbackHandler)
    thread = threading.Thread(target=server.handle_request, daemon=True)
    thread.start()

    query = parse.urlencode(
        {
            "client_id": args.client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": SCOPE,
            "access_type": "offline",
            "prompt": "consent",
            "state": state,
        }
    )
    url = f"{AUTH_URL}?{query}"
    print("Open this URL and approve Gmail send-only access:\n")
    print(url)
    try:
        webbrowser.open(url)
    except Exception:
        pass

    thread.join()
    server.server_close()
    result = CallbackHandler.result
    if result.get("error"):
        raise SystemExit(f"OAuth authorization failed: {result['error']}")
    code = result.get("code")
    if not code:
        raise SystemExit("OAuth authorization returned no code")

    tokens = exchange_code(args.client_id, args.client_secret, code, redirect_uri)
    refresh_token = tokens.get("refresh_token")
    if not refresh_token:
        raise SystemExit(
            "Google returned no refresh_token. Revoke the app grant and run again with prompt=consent."
        )

    print("\nOAuth2 authorization succeeded. Add these values to GitHub Actions secrets:")
    print("GMAIL_OAUTH_CLIENT_ID = <the client id you used>")
    print("GMAIL_OAUTH_CLIENT_SECRET = <the client secret you used>")
    print(f"GMAIL_OAUTH_REFRESH_TOKEN = {refresh_token}")
    print("GMAIL_SENDER = <the Gmail address you authorized>")
    print("\nDo not commit or share the refresh token.")


if __name__ == "__main__":
    main()
