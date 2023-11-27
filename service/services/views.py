from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from services.models import *
from services.serializers import *


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().prefetch_related('client').prefetch_related('client__user')
    serializer_class = SubscriptionSerializer

