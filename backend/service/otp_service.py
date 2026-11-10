import secrets
import time

# dictionary to store OTP data(email, otp, expiration time, attempts, verified) in memory
otp_data = {}


def create_otp(email):
    email = email.strip().lower()
    now = time.time()

    saved_otp = otp_data.get(email)

    if saved_otp and not saved_otp["verified"] and now - saved_otp["last_sent_at"] < 60:
        raise ValueError("Please wait before requesting another OTP.")

    otp = f"{secrets.randbelow(1000000):06d}"

    otp_data[email] = {
        "code": otp,
        "expires_at": now + 300,
        "last_sent_at": now,
        "attempts": 0,
        "verified": False
    }

    return otp

def verify_otp(email, entered_otp):
    email = email.strip().lower()
    saved_otp = otp_data.get(email)

    if saved_otp is None:
        return False

    if time.time() >= saved_otp["expires_at"]:
        del otp_data[email]
        return False

    if saved_otp["verified"]:
        return True

    if saved_otp["code"] != entered_otp:
        saved_otp["attempts"] += 1

        if saved_otp["attempts"] >= 5:
            del otp_data[email]

        return False

    saved_otp["code"] = None
    saved_otp["verified"] = True
    return True


def is_email_verified(email):
    email = email.strip().lower()
    saved_otp = otp_data.get(email)

    if saved_otp is None:
        return False

    if time.time() >= saved_otp["expires_at"]:
        del otp_data[email]
        return False

    return saved_otp["verified"]


def clear_verified_email(email):
    email = email.strip().lower()
    saved_otp = otp_data.get(email)

    if saved_otp is not None and saved_otp["verified"]:
        del otp_data[email]


def remove_otp(email):
    email = email.strip().lower()

    if email in otp_data:
        del otp_data[email]
