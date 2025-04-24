import django_filters
from .models import InventoryItem

class InventoryItemFilter(django_filters.FilterSet):
    user_name = django_filters.CharFilter(lookup_expr='icontains')
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = InventoryItem
        fields = [
                  'objects_name', 
                  'inventory_number', 
                  'accountable_user', 
                  'base', 
                  'office',
                  'start_data',
                  ]