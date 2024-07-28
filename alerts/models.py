from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TargetPriceOfCoin(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    coin_id = models.AutoField(primary_key=True)
    coin = models.CharField(max_length=100)
    target_price = models.DecimalField(max_digits=20, decimal_places=2)
    
    def __str__(self):
        return f"{self.user.username} - {self.coin} - {self.target_price}"
    
class TriggeredAlerts(models.Model):
    coin = models.ForeignKey(TargetPriceOfCoin, on_delete=models.CASCADE)
    alert_id = models.AutoField(primary_key=True)
    coin_name = models.CharField(max_length=50)
    target = models.DecimalField(max_digits=20, decimal_places=10)
    time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.coin.coin} - {self.target}"


class Views(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    alert = models.ForeignKey(TriggeredAlerts, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} viewed {self.alert.coin_name} at {self.alert.time}"