# serializers.py
from rest_framework import serializers
from .models import TargetPriceOfCoin, TriggeredAlerts, Views

class TargetPriceOfCoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetPriceOfCoin
        fields = '__all__'

class TriggeredAlertsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TriggeredAlerts
        fields = '__all__'

class ViewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Views
        fields = '__all__'
