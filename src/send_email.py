import smtplib
import os
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
TO_EMAIL = os.getenv("TO_EMAIL")

def _send_smtp(subject, html_content, recipient):
    """Internal helper to handle the actual SMTP transaction."""
    if not all([EMAIL_USER, EMAIL_PASS, recipient]):
        raise EnvironmentError("Missing required email environment variables or recipient.")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = EMAIL_USER
    msg["To"] = recipient

    msg.attach(MIMEText(html_content, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)

def send_email(subject, html_content):
    """Sends the newsletter email to the subscriber list (TO_EMAIL)."""
    try:
        # Newsletter goes to the configured subscriber/list
        _send_smtp(subject, html_content, TO_EMAIL)
        print(f"✅ Email sent: {subject} to {TO_EMAIL}")
    except Exception as e:
        print(f"❌ Failed to send newsletter email: {e}")
        raise  # Re-raise to ensure the main process knows it failed

def notify_failure(stage: str, error_detail: str):
    """
    Sends an error notification email ONLY to the admin (EMAIL_USER).
    """
    subject = f"❌ Automated Newsletter Failed: {stage}"
    
    # Simple, clean HTML for the error notice
    html_body = f"""
    <html>
        <body style="font-family: sans-serif; padding: 20px; color: #333;">
            <h2 style="color: #d9534f;">Newsletter Generation Failed</h2>
            <p>The automated newsletter system encountered a critical error and stopped to prevent sending incorrect data.</p>
            
            <div style="background-color: #f8d7da; color: #721c24; padding: 15px; border-radius: 5px; border: 1px solid #f5c6cb; margin: 20px 0;">
                <strong>Failed Stage:</strong> {stage}<br>
                <strong>Error Details:</strong><br>
                <pre style="white-space: pre-wrap; font-family: monospace;">{error_detail}</pre>
            </div>
            
            <p>Please check the system logs for the full traceback.</p>
        </body>
    </html>
    """

    print(f"⚠️ Attempting to send failure notification to ADMIN ({EMAIL_USER}) for stage: {stage}")
    try:
        # Error notification sends to SELF (EMAIL_USER) or could be a separate ADMIN_EMAIL if configured.
        # Request asked to send to EMAIL_USER id.
        _send_smtp(subject, html_body, EMAIL_USER)
        print("✅ Failure notification email sent to admin.")
    except Exception as e:
        print(f"CRITICAL: Failed to send failure notification email!")
        print(traceback.format_exc())

if __name__ == "__main__":
    # Test execution
    try:
        send_email("Test Subject", "<h1>Test Body</h1>")
    except Exception as e:
        notify_failure("Manual Test", str(e))
