from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from alerts.models import TargetPriceOfCoin, TriggeredAlerts, Views
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_mail(subject, message, from_email, recipient_list):
    message = Mail(
        from_email=from_email,
        to_emails=recipient_list,
        subject=subject,
        plain_text_content=message)
    try:
        sg = SendGridAPIClient("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")
        response = sg.send(message)
        print("Email sent to", recipient_list)
    except Exception as e:
        print(e)
        

@shared_task
def trigger_alert(email, symbol, price, coin_id):
    # Send email or print to console
    subject = f"Price Alert: {symbol}"
    message = f"The price of {symbol} has fallen to {price}"
    from_email = "nishanth.chennai44@gmail.com"
    recipient_list = [email]
    
   
    send_mail(subject, message, from_email, recipient_list)

    # For now, just print to console
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
