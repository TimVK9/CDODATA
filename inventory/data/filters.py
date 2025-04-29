from django_filters import rest_framework as filters
from django_filters import DateFilter, FilterSet
from django import forms
from .models import BaseInfo, InventoryItem


class InventoryItemFilter(filters.FilterSet):
    """
    Фильтр для инвентаризационных объектов
    """

    # Фильтрация по инвентаризационному объекту с поиском по подстроке
    objects_name = filters.CharFilter(
        field_name='objects_name',
        lookup_expr='icontains',
        label=''
    )

    # Фильтрация по инвентаризационному номеру
    inventory_number = filters.CharFilter(
        lookup_expr='icontains',
        label=''
    )

    # Фильтрация по подразделению
    base = filters.ModelChoiceFilter(
        queryset=BaseInfo.objects.all(),
        label=''
    )

    # Фильтрация по кабинету с числовым диапазоном
    office = filters.NumberFilter(
        label=''
    )

    # Фильтрация по ответственному лицу
    accountable_user = filters.CharFilter(
        field_name='accountable_user',
        lookup_expr='icontains',
        label=''
    )

    # Фильтрация по дате ввода в эксплуатацию
    start_data = filters.DateFilter(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label=''
    )

    # Фильтрация по диапазону дат
    start_data_gte = filters.DateFilter(
        field_name='start_data',
        lookup_expr='gte',
        help_text="Дата ввода от",
        widget=forms.DateInput(attrs={'type': 'date'}),
        label=''
    )

    start_data_lte = filters.DateFilter(
        field_name='start_data',
        lookup_expr='lte',
        help_text="Дата ввода до",
        widget=forms.DateInput(attrs={'type': 'date'}),
        label=''
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
        
        # Добавляем упорядочивание полей для корректного отображения в форме
        ordering = [
            'objects_name',
            'inventory_number',
            'base',
            'office',
            'accountable_user',
            'start_data',
            'start_data_gte',
            'start_data_lte'
        ]
