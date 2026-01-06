import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from build_newsletter import build_html

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
TO_EMAIL = os.getenv("TO_EMAIL")

def send_email():
    html_content = build_html()

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "📰 Weekly Tech Newsletter"
    msg["From"] = EMAIL_USER
    msg["To"] = TO_EMAIL

    msg.attach(MIMEText(html_content, "html"))

    if not all([EMAIL_USER, EMAIL_PASS, TO_EMAIL]):
        print("⚠️  Missing email credentials (EMAIL_USER, EMAIL_PASS, TO_EMAIL).")
        print("✅ Simulating email send...")
        print(f"Subject: {msg['Subject']}")
        print(f"To: {msg['To']}")
        print("Email content generated successfully in 'newsletter_output.html'")
        return

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

if __name__ == "__main__":
    send_email()
