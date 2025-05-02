from django.forms import ValidationError
from .var import *
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.core.validators import MinLengthValidator
from .validate import validate_number_int, validate_description_length
import logging
from django.db import transaction
class BaseInfo(models.Model):
    """Модель для хранения информации о подразделениях"""
    base_name = models.CharField(
        max_length=64,
        verbose_name="Название подразделения",
        unique=True,
    )
    base_address = models.CharField(
        max_length=255,
        verbose_name="Адрес подразделения",
    )
    logo = models.ImageField(
        upload_to='titles/',
        verbose_name="Логотип подразделения",
        blank=True,
        null=True,
    )

    def get_absolute_url(self):
        return reverse('baseinfo-detail', kwargs={'pk': self.pk})
    
    def __str__(self):
        return f'{self.base_name}'

    class Meta:
        verbose_name = "Подразделение"
        verbose_name_plural = "Подразделения"


class InventoryItem(models.Model):
    """Модель для учета инвентарных объектов"""
    IN_USE = 'Введено в эксплуатацию'
    RETIRED = 'Снято с учёта'
    
    STATE_CHOICES = [
        (IN_USE, 'Введено в эксплуатацию'),
        (RETIRED, 'Снято с учёта')
    ]

    state = models.CharField(
        max_length=40,
        choices=STATE_CHOICES,
        default=IN_USE,
        verbose_name='Состояние учёта'
    )
    
    objects_name = models.CharField(
        max_length=128,
        verbose_name="Инвентаризационный объект",

    )
    
    inventory_number = models.CharField(
        max_length=12,
        verbose_name="Инвентаризационный номер",
        validators=[validate_number_int],
        unique=True
    )
    
    value = models.CharField(
        choices=ACCOUNT_CHOICES,
        max_length=20,  
        default='00.00.00.00',
        verbose_name="Счет актива"
    )

    
    
    base = models.ForeignKey(
        BaseInfo,
        on_delete=models.PROTECT,
        verbose_name="Подразделение",
        related_name='inventory_items'
    )
    
    office = models.CharField(
        max_length=10,
        default="0",
        verbose_name="Кабинет расположения",

    )
    
    accountable_user = models.CharField(
        max_length=255,
        verbose_name='Ответственный за содержание',

    )
    
    start_date = models.DateField(
        verbose_name="Дата ввода в эксплуатацию",
       
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания записи"
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата последнего изменения"
    )
    
    description = models.TextField(
        verbose_name="Описание",
        validators=[validate_description_length],
        default='''Здесь должно быть описание объекта, позволяющее легко его идентифицировать.
                Здесь могут быть его характеристики, цвет, объем, системные данные и т.п.''',
        
    )
    
    current_duration = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Срок эксплуатации (дни)",
        editable=False

    )
    
    


    def bulk_update_start_dates(self):
        items = InventoryItem.objects.all()
        for item in items:
                # Здесь можно добавить логику изменения start_date если нужно
                # Например: item.start_date = new_date
            item.save()  # автоматически вызовет пересчёт current_duration
        return f"Обновлено {items.count()} записей"
    
    def save(self, *args, **kwargs):
        """Переопределение метода save для обработки инвентарного номера и расчёта срока эксплуатации"""
        # Заполнение инвентарного номера нулями слева, если он меньше 12 символов
        if self.inventory_number and len(self.inventory_number) < 12:
            self.inventory_number = self.inventory_number.zfill(12)
        
        # Расчёт срока эксплуатации в днях
        if self.start_date:
            self.current_duration = (timezone.now().date() - self.start_date).days
        
        super().save(*args, **kwargs)

    def update_duration(self):
        """Метод для обновления срока эксплуатации"""
        if self.start_date:
            self.current_duration = (timezone.now().date() - self.start_date).days
            self.save(update_fields=['current_duration'])

    def clean(self):
        """Валидация модели"""
        super().clean()
        

        if self.inventory_number:

            self.inventory_number = self.inventory_number.strip()

            if len(self.inventory_number) < 12:
                self.inventory_number = self.inventory_number.zfill(12)

    def get_absolute_url(self):
        return reverse('inventoryitem-detail', kwargs={'pk': self.pk})


    def __str__(self):
        return (
            f"{self.objects_name} (инв. №{self.inventory_number}) - "
            f"{self.base.base_name}, каб. {self.office}"
        )

    class Meta:
        verbose_name = "Инвентаризационная запись"
        verbose_name_plural = "Инвентаризационные записи"
        ordering = ['-created_at']


class QrCode(models.Model):
    """Модель для хранения QR-кодов инвентарных объектов"""
    objects_item = models.OneToOneField(
        InventoryItem,
        on_delete=models.CASCADE,
        verbose_name="Инвентарный объект",
        related_name='qr_code'
    )
    
    qr = models.ImageField(
        upload_to='qr_codes/%Y/%m/%d/',
        verbose_name="QR-код",
        help_text="QR-код инвентарного объекта"
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания QR-кода"
    )

    def __str__(self):
        return f'QR-код для {self.objects_item}'

    class Meta:
        verbose_name = "QR-код"
        verbose_name_plural = "QR-коды"
        ordering = ['-created_at']