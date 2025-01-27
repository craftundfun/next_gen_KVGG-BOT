import os
from email.message import EmailMessage
import smtplib


def send_exception_mail(message: str):
    if not bool(int(os.getenv("PRODUCTION"))):
        return

    exception_recipients = ["bjarneblu@gmail.com"]
    subject = "Critical Error in KVGG-Bot-Python"

    for exception_recipient in exception_recipients:
        email = EmailMessage()
        email["From"] = "KVGG-Bot-Python"
        email["To"] = exception_recipient
        email["Subject"] = subject
        email.set_content(f"Stacktrace: {message}")

        try:
            with smtplib.SMTP_SSL(os.getenv("EMAIL_SERVER"), int(os.getenv("EMAIL_PORT"))) as server:
                server.login(os.getenv("EMAIL_USERNAME"), os.getenv("EMAIL_PASSWORD"))
                server.send_message(email)
        except Exception as error:
            print("An error occurred while sending an email!\n", error)

            continue
