import django_filters
from django import forms
from .models import InventoryItem, BaseInfo
from .var import ACCOUNT_CHOICES


class InventoryItemFilter(django_filters.FilterSet):
    """Фильтр для инвентарных объектов с улучшенным UI"""
    
    # Основные фильтры
    objects_name = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Название объекта',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Введите название...'
        })
    )
    
    inventory_number = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Инвентарный номер',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Введите номер...'
        })
    )
    
    base = django_filters.ModelChoiceFilter(
        queryset=BaseInfo.objects.all().order_by('base_name'),
        label='Подразделение',
        widget=forms.Select(attrs={
            'class': 'form-select form-select-sm'
        })
    )
    
    state = django_filters.ChoiceFilter(
        choices=InventoryItem.STATE_CHOICES,
        label='Состояние',
        widget=forms.Select(attrs={
            'class': 'form-select form-select-sm'
        })
    )
    
    value = django_filters.ChoiceFilter(
        lookup_expr='icontains',
        choices=InventoryItem.value,
        label='Счет актива',
        widget=forms.Select(attrs={
            'class': 'form-select form-select-sm'
        })
    )
    
    office = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Кабинет',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'Номер кабинета...'
        })
    )
    
    accountable_user = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Ответственный',
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-sm',
            'placeholder': 'ФИО ответственного...'
        })
    )
    
    # Фильтры по дате
    start_date = django_filters.DateFilter(
        field_name='start_date',
        lookup_expr='exact',
        label='Дата ввода',
        widget=forms.DateInput(attrs={
            'class': 'form-control form-control-sm',
            'type': 'date'
        })
    )
    
    start_date_before = django_filters.DateFilter(
        field_name='start_date',
        lookup_expr='lte',
        label='Дата ввода до',
        widget=forms.DateInput(attrs={
            'class': 'form-control form-control-sm',
            'type': 'date'
        })
    )
    
    start_date_after = django_filters.DateFilter(
        field_name='start_date',
        lookup_expr='gte',
        label='Дата ввода после',
        widget=forms.DateInput(attrs={
            'class': 'form-control form-control-sm',
            'type': 'date'
        })
    )
    
    value = django_filters.ChoiceFilter(
        choices=ACCOUNT_CHOICES,
        label='Счёт актива',

    )

    class Meta:
        model = InventoryItem
        fields = [
            'objects_name',
            'inventory_number',
            'base',
            'state',
            'office',
            'accountable_user',
            'start_date',
            'value'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Установка placeholder'ов для всех текстовых полей
        for field_name, field in self.filters.items():
            if isinstance(field, django_filters.CharFilter):
                if 'placeholder' not in field.field.widget.attrs:
                    field.field.widget.attrs['placeholder'] = f'Фильтр по {field.label.lower()}...'
            
            # Добавление классов Bootstrap по умолчанию
            if 'class' not in field.field.widget.attrs:
                if isinstance(field.field.widget, forms.Select):
                    field.field.widget.attrs['class'] = 'form-select form-select-sm'
                else:
                    field.field.widget.attrs['class'] = 'form-control form-control-sm'