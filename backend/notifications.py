import smtplib
from email.mime.text import MIMEText
def create_email_notification(alert_type, severity, shipment_id, location, message):

    email = {
        "to": "supply.manager@company.com",

        "subject": f"{severity} Alert - {alert_type}",

        "body": f"""
Smart Supply Chain Alert

Shipment: {shipment_id}
Location: {location}
Severity: {severity}
Alert Type: {alert_type}

Message:
{message}

Recommended Action:
Please check the shipment immediately.
"""
    }

    return email
EMAIL_SENDER = "anousheh.naderi98@gmail.com"
EMAIL_PASSWORD = "ixzr mkiq ljyn mnyi"
EMAIL_RECEIVER = "anousheh.naderi98@gmail.com"


def send_email_alert(subject, body):
    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER

    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
    print("Mail successfully sent")