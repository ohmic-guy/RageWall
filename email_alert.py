import smtplib
from email.mime.text import MIMEText

def send_alert(subject, body, to_email, from_email, from_password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(from_email, from_password)
            server.send_message(msg)
        print(f"Alert sent to {to_email}")
    except Exception as e:
        print(f"Failed to send alert: {e}")

# Example usage:
send_alert(
    subject="RageWall Alert",
    body="Suspicious activity detected!",
    to_email="omkarankit2004@gmail.com",
    from_email="replitbaya@gmail.com",
    from_password="Ankit@replitBaya"
)