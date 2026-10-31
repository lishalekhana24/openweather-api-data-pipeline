import os
import smtplib
from email.message import EmailMessage

sender_email = os.environ.get("GMAIL_SENDER")
receiver_email = os.environ.get("GMAIL_RECEIVER")
app_password = os.environ.get("GMAIL_APP_PASSWORD")

if not sender_email or not receiver_email or not app_password:
    raise RuntimeError("Gmail email settings are not fully configured.")

message = EmailMessage()
message["Subject"] = "OpenWeather Project - Success"
message["From"] = sender_email
message["To"] = receiver_email
message.set_content(
    "Your Hyderabad weather pipeline completed successfully. "
    "The output CSV passed validation."
)

with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=30) as server:
    server.login(sender_email, app_password.replace(" ", ""))
    server.send_message(message)

print("Success email sent!")
