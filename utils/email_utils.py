# utils/email_utils.py
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import random
import os

def send_otp_email(receiver_email, name):
    OTP = ''.join([str(random.randint(0, 9)) for _ in range(6)])

    subject = "🔐 Forgot Password - OTP Verification - Password Manager"
    body = (
        f"Dear {name},\n\n"
        f"You have requested to reset your password.\n"
        f"Your One-Time Password (OTP) is: {OTP}\n\n"
        "Please enter this OTP in the Password Manager app to proceed.\n"
        "Do not share this OTP with anyone.\n\n"
        "If you did not request this, please ignore this message.\n\n"
        "Regards,\n"
        "Password Manager Team"
    )
    # message = f"Subject: {subject}\n\n{body}"

    try:
        sender_email = os.getenv("EMAIL_SENDER")
        sender_password = os.getenv("EMAIL_PASSWORD")

        if not sender_email or not sender_password:
            print("⚠️ EMAIL_SENDER or EMAIL_PASSWORD not set in environment variables.")
            return None

        # Create email message using UTF-8 encoding
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain", "utf-8"))  # ✅ Ensures emoji/unicode support

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()

        print(f"✅ OTP sent to {receiver_email}")
        return OTP

    except Exception as e:
        print("❌ Failed to send email:", e)
        return None





def send_otp_email_view(receiver_email):
    OTP = ''.join([str(random.randint(0, 9)) for _ in range(6)])

    subject = "🔐 OTP Verification to View Saved Password - Password Manager"
    body = (
        f"Your OTP is: {OTP}\n\n"
        "This OTP is required to view your saved password.\n"
        "Do not share this with anyone."
        "If you did not request this, please ignore this message.\n\n"
        "Regards,\n"
        "Password Manager Team"
    )

    # Construct MIME Email with UTF-8 encoding
    message = MIMEMultipart()
    message["From"] = os.getenv("EMAIL_SENDER")
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain", "utf-8"))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        sender_email = os.getenv("EMAIL_SENDER")
        sender_password = os.getenv("EMAIL_PASSWORD")

        if not sender_email or not sender_password:
            print("⚠️ EMAIL_SENDER or EMAIL_PASSWORD not set in environment variables.")
            return None

        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()

        print(f"✅ OTP sent to {receiver_email}")
        return OTP

    except Exception as e:
        print("❌ Failed to send email:", e)
        return None
