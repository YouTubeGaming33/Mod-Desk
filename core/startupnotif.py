import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from datetime import datetime

from core.config import GMAIL_PASSWORD

now = datetime.now()
formatted = now.strftime("%Y-%m-%d %H:%M:%S")

def send_startup_email():
    sender_email = "wobblewibble03@gmail.com"
    receiver_email = "wobblewibble03@gmail.com"  # You can send it to yourself
    password = GMAIL_PASSWORD

    # Create the email
    message = MIMEMultipart("alternative")
    message["Subject"] = "Mod-Desk Booted - Production"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Email content
    text = f"Mod-Desk Bot has Successfully Booted for Production Use.\n\nStartup Information: {formatted}"
    part = MIMEText(text, "plain")
    message.attach(part)

    # Connect and send
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Startup email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
