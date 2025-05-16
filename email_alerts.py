'''function below is an example of configuring email alerts'''

import smtplib
from email.mime.text import MIMEText

def send_email(subject, body):
    sender = "your_email@gmail.com"
    recipient = "recepient_email@gmail.com"
    password = "your password" #consider using environment variable for this field

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipient

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())
