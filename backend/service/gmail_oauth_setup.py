from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow


SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
PROJECT_ROOT = Path(__file__).resolve().parents[2]
CLIENT_SECRETS_FILE = PROJECT_ROOT / "credentials.json"
TOKEN_FILE = PROJECT_ROOT / "gmail_token.json"


def main():
    if not CLIENT_SECRETS_FILE.is_file():
        raise SystemExit(
            "OAuth client file not found. Download the Desktop app client JSON "
            "from Google Cloud Console and save it as credentials.json in the project root."
        )

    flow = InstalledAppFlow.from_client_secrets_file(
        str(CLIENT_SECRETS_FILE),
        SCOPES
    )
    credentials = flow.run_local_server(
        host="localhost",
        port=0,
        access_type="offline",
        prompt="consent"
    )

    TOKEN_FILE.write_text(credentials.to_json(), encoding="utf-8")
    print(f"Gmail OAuth token saved to {TOKEN_FILE}")


if __name__ == "__main__":
    main()