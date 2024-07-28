from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def trigger_alert(email, symbol, price):
    # Send email or print to console
    subject = f"Price Alert: {symbol}"
    message = f"The price of {symbol} has fallen to {price}"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    
    # dont have time.. sorry :) i thought of using twillo API but i dont have time to implement it
    
    # send_mail(subject, message, from_email, recipient_list)

    # For now, just print to console
    print(f"Alert: {subject} - {message}")
