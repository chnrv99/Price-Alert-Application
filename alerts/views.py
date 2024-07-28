# views.py
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import TargetPriceOfCoin, TriggeredAlerts, Views
from .serializers import TargetPriceOfCoinSerializer, TriggeredAlertsSerializer, ViewsSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

class CreateAlertView(generics.CreateAPIView):
    queryset = TargetPriceOfCoin.objects.all()
    serializer_class = TargetPriceOfCoinSerializer
    permission_classes = [IsAuthenticated]

class DeleteAlertView(generics.DestroyAPIView):
    queryset = TargetPriceOfCoin.objects.all()
    serializer_class = TargetPriceOfCoinSerializer
    permission_classes = [IsAuthenticated]

class FetchAlertsView(generics.ListAPIView):
    queryset = TargetPriceOfCoin.objects.all()  # Default queryset
    serializer_class = TargetPriceOfCoinSerializer  # Default serializer

    def get_queryset(self):
        alert_type = self.request.query_params.get('type')
        page = self.request.query_params.get('page', 1)
        start = (int(page) - 1) * 3
        end = int(page) * 3

        if alert_type == 'target_price':
            queryset = TargetPriceOfCoin.objects.all()[start:end]
            self.serializer_class = TargetPriceOfCoinSerializer
        elif alert_type == 'triggered_alerts':
            queryset = TriggeredAlerts.objects.all()[start:end]
            self.serializer_class = TriggeredAlertsSerializer
        elif alert_type == 'views':
            queryset = Views.objects.all()[start:end]
            self.serializer_class = ViewsSerializer
        else:
            queryset = []
        
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            return Response({'error': 'Invalid alert type'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @method_decorator(cache_page(60*2)) # Cache the response for 2 minutes
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)