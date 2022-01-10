import django_filters
from django_filters import RangeFilter

from .models import *


class OrderFilter(django_filters.FilterSet):
    Month_Amount = RangeFilter(field_name='amount_per_month', lookup_expr='lte')

    class Meta:
        model = Property_registration
        fields = '__all__'
        exclude = ['property_image', 'property_name', 'amount_per_month', 'detail', 'available', 'owner_name',
                   'time_added']
