from email.message import EmailMessage
import ssl
import smtplib

def send_email(email_reciver, subject, body):
    email_sender = "automatyzacjakurs@gmail.com"
    email_password = "nedn svmx zkby ddqv"


    msg = EmailMessage()
    msg["From"] = email_sender
    msg["To"] = email_reciver
    msg["Subject"] = subject
    msg.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(email_sender, email_password)
        server.sendmail(email_sender, email_reciver, msg.as_string())

