from django_filters import rest_framework as filters
from .models import BaseInfo, InventoryItem
from django_filters import ChoiceFilter
from django import forms
from django_filters import DateFilter, FilterSet

class InventoryItemFilter(filters.FilterSet):
    
    # Фильтрация по инвентаризационному объекту с поиском по подстроке
    objects_name = filters.CharFilter(
        field_name='objects_name',
        lookup_expr='icontains',
        help_text="Поиск по названию объекта",

    )
    
    # Фильтрация по инвентаризационному номеру
    inventory_number = filters.CharFilter(
        help_text="Введите инвентаризационный номер",
        lookup_expr='icontains',
    )
    
      
    # Фильтрация по подразделению
    base = filters.ModelChoiceFilter(
        queryset=BaseInfo.objects.all(),
        help_text="Выберите подразделение"
    )
    
    # Фильтрация по кабинету с числовым диапазоном
    office = filters.NumberFilter(
        help_text="Введите номер кабинета"
    )
    
    # Фильтрация по ответственному лицу
    accountable_user = filters.CharFilter(
        field_name='accountable_user',
        lookup_expr='icontains',
        help_text="Поиск по ответственному лицу"
    )
    
    # Фильтрация по дате ввода в эксплуатацию
    start_data = filters.DateFilter(
        help_text="Введите дату ввода в эксплуатацию",
        widget=forms.DateInput(attrs={'type': 'date'})  # Добавляем виджет для выбора даты
    )
    
    # Фильтрация по диапазону дат
    start_data_gte = filters.DateFilter(
        field_name='start_data',
        lookup_expr='gte',
        help_text="Дата ввода от",
        widget=forms.DateInput(attrs={'type': 'date'})  # Добавляем виджет для выбора даты
    )
    
    start_data_lte = DateFilter(
        field_name='start_data',
        lookup_expr='lte',
        help_text="Дата ввода до",
        widget=forms.DateInput(attrs={'type': 'date'})  # Добавляем виджет для выбора даты
    
    )
    
    class Meta:
        model = InventoryItem
        fields = [
            'objects_name',
            'inventory_number',
            'base',
            'office',
            'accountable_user',
            'start_data',
            'start_data_gte',
            'start_data_lte'
        ]
