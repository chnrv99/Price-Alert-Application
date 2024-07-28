from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from alerts.models import TargetPriceOfCoin, TriggeredAlerts, Views

@shared_task
def trigger_alert(email, symbol, price, coin_id):
    # Send email or print to console
    subject = f"Price Alert: {symbol}"
    message = f"The price of {symbol} has fallen to {price}"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    
    # dont have time.. sorry :) i thought of using twillo API but i dont have time to implement it
    
    # send_mail(subject, message, from_email, recipient_list)

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
