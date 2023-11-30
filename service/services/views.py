from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from services.models import *
from services.serializers import *
from clients.models import Client
from django.db.models import Prefetch, F, Sum


class SubscriptionView(ReadOnlyModelViewSet):
    queryset = Subscription.objects.all().prefetch_related(
        'plan',
        Prefetch('client',
                 queryset=Client.objects.all().select_related('user').only('company_name',
                                                              'user__email')))
        # .annotate(price=
        #                                                     F('service__full_price') -
        #                                                     F('service__full_price') *
        #                                                     F('plan__discount_percent')/100.00)
    serializer_class = SubscriptionSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        responce = super().list(request, *args, **kwargs)

        responce_data = {'result': responce.data}
        responce_data['total_amount'] = queryset.aggregate(total=Sum('price')).get('total')
        responce.data = responce_data

        return responce

