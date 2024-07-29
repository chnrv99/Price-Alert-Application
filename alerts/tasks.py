import threading
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from alerts.models import TargetPriceOfCoin, TriggeredAlerts, Views
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Create a lock for the send_mail function
send_mail_lock = threading.Lock()

def send_mail(subject, message, from_email, recipient_list):
    # Gmail SMTP server address
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    # Your Gmail account credentials
    gmail_user = "nishanth.work99@gmail.com"
    gmail_password = "ecny wrar rdsu oscc"  # Use the app-specific password

    # Create the email headers and body
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ", ".join(recipient_list)
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    with send_mail_lock:
        try:
            # Connect to the Gmail SMTP server and send the email
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(gmail_user, gmail_password)
            server.sendmail(from_email, recipient_list, msg.as_string())
            server.quit()
            print("Email sent to", recipient_list)
        except Exception as e:
            print("Failed to send email:", e)

@shared_task
def trigger_alert(email, symbol, price, coin_id):
    # Send email or print to console
    subject = f"Price Alert: {symbol}"
    message = f"The price of {symbol} has fallen to {price}"
    from_email = "nishanth.chennai44@gmail.com"
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)
    print(f"Alert: {subject} - {message}")

    # make the flag_trigger True
    target = TargetPriceOfCoin.objects.get(coin_id=coin_id)
    target.flag_trigger = True
    target.save()
    print("Flag Trigger set to True for coin_id:", target.coin_id)

    # add that record to TriggeredAlerts
    triggered_alert = TriggeredAlerts(coin=target, coin_name=symbol, target=target.target_price)
    triggered_alert.save()
    print("Triggered Alert saved")

    # add that record to Views
    view = Views(user=target.user, alert=triggered_alert)
    view.save()
    print("View saved")
