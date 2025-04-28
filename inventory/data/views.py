from django.shortcuts import render
from django.views.generic import (ListView, DetailView,
                                  CreateView, UpdateView,
                                  DeleteView)

from .models import InventoryItem
from .filters import InventoryItemFilter
from django.core.paginator import Paginator
from . forms import *
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import BaseInfo, InventoryItem
from django.urls import reverse_lazy


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

class CreateView(CreateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'inventoryitem_create.html'
    success_url = '/' 
    
class InventoryUpdate(UpdateView):
    form_class = InventoryItemForm
    model = InventoryItem
    template_name = 'update.html'
    success_url = '/'
    


class InventoryItemtDelete(DeleteView):
    model = InventoryItem
    template_name = 'delete_inventory_item.html'
    success_url = '/'    
 
class ObjectDetail(DetailView):
    model = InventoryItem
    context_object_name = 'inventory_object'
    template_name = 'detail.html'
 
 

def inventory_item_list_view(request):
    item_filter = InventoryItemFilter(request.GET, queryset=InventoryItem.objects.all())
    paginator = Paginator(item_filter.qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'inventoryitem_list.html', {'filter': item_filter, 'page_obj': page_obj})




def import_excel(request):
    if request.method == 'POST' and request.FILES.get('excel_file'):
        excel_file = request.FILES['excel_file']
        
        # Читаем Excel файл
        df = pd.read_excel(excel_file)

        # Создаем подразделения, если их нет
        bases = {}
        for _, row in df.iterrows():
            base_name = row['Название подразделения']
            if base_name not in bases:
                base, created = BaseInfo.objects.get_or_create(
                    base_name=base_name,
                    base_addres=row['Адрес подразделения']
                )
                bases[base_name] = base


        
        # Создаем инвентаризационные записи
        for _, row in df.iterrows():
            inventory_item, created = InventoryItem.objects.get_or_create(
                state=row['Состояние учёта'],
                objects_name=row['Инвентаризационный объект'],
                inventory_number=row['Инвентаризационный номер'],
                value=row['Счёт'],
                base=bases[row['Название подразделения']],
                office=row['Кабинет расположения'],
                accountable_user=row['Ответственный за содержание'],
                start_data=row['Введен в эксплуатацию'],
                discription=row['Введен в эксплуатацию']               
                
            )
            
        
        messages.success(request, 'Данные успешно импортированы')
        return redirect('inventoryitem_list')
    
    return render(request, 'exel_imp.html')



