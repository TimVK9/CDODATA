from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from django.utils import timezone
from .validate import *

class BaseInfo(models.Model):
    base_name = models.CharField(
        max_length=64,
        verbose_name="Название подразделения",
        unique=True
    )
    base_addres = models.CharField(
        max_length=255,
        verbose_name="Адрес подразделения"
    )

    def __str__(self):
        return f"{self.base_name}"

    class Meta:
        verbose_name = "Подразделение"
        verbose_name_plural = "Подразделения"


class InventoryItem(models.Model):
    STATE_CHOICES = [
        
        ('Введено в эксплуатацию', 'Введено в эксплуатацию'),
        ('Снято с учёта', 'Снято с учёта')
    ]

    state = models.CharField(
        max_length=40,
        choices=STATE_CHOICES,
        default='Введено в эксплуатацию', 
        verbose_name='Состояние учёта'
    )
    
    objects_name = models.CharField(
            max_length=128,
            verbose_name="Инвентаризационный объект"
        
    )
    
    inventory_number = models.CharField(
                        verbose_name="Инвентаризационный номер",
                        help_text="Введите значение до 12 цифр"
    )
    
    value = models.CharField(
        max_length=500,
        verbose_name="Счёт"
    )
    
    base = models.ForeignKey(
        BaseInfo,
        on_delete=models.CASCADE,
        verbose_name="Подразделение"
    )
    
    office = models.CharField(
        null=False,
        default="0",
        verbose_name="Кабинет расположения"
    )
    
    accountable_user = models.CharField(
        max_length=255,
        verbose_name='Ответственный за содержание'
    )
    
    start_data = models.DateField(  
        verbose_name="Дата ввода в эксплуатацию",
       
    )

    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Объект создан")
    
    updated_at = models.DateTimeField(auto_now=True, editable=False,
                                      verbose_name="Последнее изменение")
    
    discription = models.TextField(verbose_name="Описание", 
                                   validators=[validate_description_length],
                                   default='''Здесь должно быть описание объекта, позволяющее лего его идентифицировать
                                   Здесь могут быть его характеристики, цвет, объем системные данные и т.п.'''
                                   )
    current_duration = models.CharField(max_length=5, 
                                        blank=True,
                                        verbose_name="Срок эксплуатации",)




    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.pk})
    
    def calculate_days_in_service(self):

        if self.state == 'Введено в эксплуатацию':

            delta = timezone.now().date() - self.start_data
  
            self.current_duration = delta

            self.save()
            return f'{delta.days}'
        return f'Выведен из эксплуатации'


    def __str__(self):
        
        return (
            f"Объект инвентаризации - {self.objects_name};\n"
            f"База - {self.base};\n"
            f"Кабинет размещения - {self.office};\n"
            f"Ответственный за содержание - {self.accountable_user}\n"
            f"Инвентаризационный номер - {str(self.inventory_number).zfill(12)};\n"
        )

    class Meta:
        verbose_name = "Инвентаризационные данные"
        verbose_name_plural = "Инвентаризационные данные"


class QrCode(models.Model):
    objects_item = models.OneToOneField(
        InventoryItem,
        on_delete=models.CASCADE,
        verbose_name="Инвентарный объект"
    )
    
    qr = models.ImageField(
        upload_to='qr_codes/',
        verbose_name="QR-код"
    )
    
    def __str__(self):  # Исправлено название метода
        return f'QR-код для {self.objects_item}'
