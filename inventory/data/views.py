from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django_filters.views import FilterView
from .models import InventoryItem
from .filters import InventoryItemFilter

class InventoryItemCreateView(CreateView):
    model = InventoryItem
    fields = ['name', 'inventory_number', 'value', 'base', 'office', 'user_name']
    template_name = 'inventoryitem_form.html'
    success_url = reverse_lazy('inventoryitem_list')

class InventoryItemListView(FilterView):
    model = InventoryItem
    template_name = 'inventoryitem_list.html'
    context_object_name = 'inventory_items'
    filterset_class = InventoryItemFilter

