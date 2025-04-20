import django_filters
from .models import InventoryItem

class InventoryItemFilter(django_filters.FilterSet):
    user_name = django_filters.CharFilter(lookup_expr='icontains')
    name = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = InventoryItem
        fields = [
                  'name', 
                  'inventory_number', 
                  'user_name', 
                  'base', 
                  'office'
                  ]