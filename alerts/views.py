# views.py
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import TargetPriceOfCoin, TriggeredAlerts, Views
from .serializers import TargetPriceOfCoinSerializer, TriggeredAlertsSerializer, ViewsSerializer
from rest_framework.permissions import IsAuthenticated

class CreateAlertView(generics.CreateAPIView):
    queryset = TargetPriceOfCoin.objects.all()
    serializer_class = TargetPriceOfCoinSerializer
    permission_classes = [IsAuthenticated]

class DeleteAlertView(generics.DestroyAPIView):
    queryset = TargetPriceOfCoin.objects.all()
    serializer_class = TargetPriceOfCoinSerializer
    # permission_classes = [IsAuthenticated]

class FetchAlertsView(generics.ListAPIView):
    queryset = Views.objects.all()
    serializer_class = ViewsSerializer
    # permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
