from django.shortcuts import render
from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView,
                                  DeleteView)
from .models import InventoryItem
from .filters import InventoryItemFilter
from django.core.paginator import Paginator
from . forms import *




class InventoryList(ListView):
    model = InventoryItem
    context_object_name = 'inventory_list'
    template_name = 'inventoryitem_list.html'

    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Создаем объект фильтра
        inventory_filter = InventoryItemFilter(self.request.GET, queryset=self.get_queryset())
        context['filter'] = inventory_filter
        return context
    
    def get_queryset(self):
        return InventoryItemFilter(self.request.GET, queryset=InventoryItem.objects.all()).qs
    
    



class InventoryItemCreateView(CreateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'inventoryitem_create.html'
    success_url = '/' 
    
class InventoryItemUpdate(UpdateView):
    form_class = InventoryItemForm
    model = InventoryItem
    template_name = 'update_inventory_item.html'
    success_url = '/'


class InventoryItemtDelete(DeleteView):
    model = InventoryItem
    template_name = 'delete_inventory_item.html'
    success_url = '/'    
 
 
 
 

def inventory_item_list_view(request):
    item_filter = InventoryItemFilter(request.GET, queryset=InventoryItem.objects.all())
    paginator = Paginator(item_filter.qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'inventoryitem_list.html', {'filter': item_filter, 'page_obj': page_obj})



