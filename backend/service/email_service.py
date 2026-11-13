import base64
import os
from email.message import EmailMessage
from pathlib import Path

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

load_dotenv()

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]
PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _get_gmail_credentials():
    token_file = Path(os.getenv("GMAIL_TOKEN_FILE", str(PROJECT_ROOT / "gmail_token.json")))
    if not token_file.is_absolute():
        token_file = PROJECT_ROOT / token_file

    if not token_file.is_file():
        raise RuntimeError(
            "Gmail OAuth token is missing. Run "
            "python -m backend.service.gmail_oauth_setup first."
        )

    credentials = Credentials.from_authorized_user_file(str(token_file), SCOPES)
    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
        token_file.write_text(credentials.to_json(), encoding="utf-8")

    if not credentials.valid:
        raise RuntimeError(
            "Gmail OAuth credentials are invalid. Re-run "
            "python -m backend.service.gmail_oauth_setup."
        )

    return credentials


def send_otp_email(email, otp):
    message = EmailMessage()
    message["Subject"] = "Your registration OTP for Campus Find"
    message["To"] = email
    message.set_content("Your OTP is " + otp + ". It expires in 5 minutes.")

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode("ascii")
    gmail = build("gmail", "v1", credentials=_get_gmail_credentials(), cache_discovery=False)
    gmail.users().messages().send(
        userId="me",
        body={"raw": encoded_message}
    ).execute()
