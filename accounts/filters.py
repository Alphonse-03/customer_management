import django_filters
from .models import *

class OrderFilterCustomer(django_filters.FilterSet):
    class Meta:
        model = Order
        fields ='__all__'
        exclude=['customer','date_created']

class OrderFilterDashboard(django_filters.FilterSet):
    class Meta:
        model = Order
        fields ='__all__'
        exclude=['date_created']