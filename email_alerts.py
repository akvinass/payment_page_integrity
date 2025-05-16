import smtplib
from email.mime.text import MIMEText

def send_email(subject, body):
    sender = "akvinass@gmail.com"
    recipient = "akvinass@gmail.com"
    password = "oclfrycrcankjogf"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())
