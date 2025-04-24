from datetime import timezone
from django.db import models

class BaseInfo(models.Model):
    
    base_name = models.CharField(max_length=64, 
                            verbose_name="Название подразделения",
                            unique=True)
    
    base_addres = models.CharField(max_length=255, 
                               verbose_name="Адрес подразделения")

    def __str__(self):
        return f"{self.base_name} - {self.base_addres}"
    
    class Meta:
        verbose_name = "Подразделение"
        verbose_name_plural = "Подразделения"
    
    
    
class InventoryItem(models.Model):

    STATE_CHOICES = [
        ('Y', 'Введено в эксплуатацию'),
        ('N', 'Снято с учёта'),

    ]

    state = models.CharField(max_length=2, 
                             choices=STATE_CHOICES, 
                             default='Введено в эксплуатацию', 
                             verbose_name='Состояние учёта')
    
    objects_name = models.CharField(max_length=128, 
                            
                            verbose_name="Инвентаризационный объект")
    
    inventory_number = models.CharField(max_length=50, 
                                        default=000000000000,
                                        

                                        verbose_name="Инвентаризационный номер")
    
    value = models.CharField(max_length=500, 
                                verbose_name="Счёт") 
    
    base = models.ForeignKey(BaseInfo, 
                             on_delete=models.CASCADE, 
                             verbose_name="Подразделение")
    
    office = models.CharField(null=False, 
                                      default="0",
                                      verbose_name="Кабинет расположения")
    
    accountable_user = models.CharField(max_length=255, 
                            verbose_name='Отвественный за содержание')
    
    start_data = models.CharField(max_length=64, verbose_name="Дата ввода в эксплуатацию")
    
    def __str__(self):
        return f'''
                   {self.objects_name};\n
                   Инвентаризационный номер - {self.inventory_number};\n
                   База - {self.base};\n
                   Кабинет размещения - {self.office};\n
                   Ответсвенный за содержание - {self.accountable_user};\n
                   
                '''
    class Meta:
        
        verbose_name = "Инвентаризационные данные"
        verbose_name_plural = "Инвентаризационные данные"
        
        
        
class QrCode(models.Model):
    objects_item = models.OneToOneField(InventoryItem, 
                                        on_delete=models.CASCADE, 
                                        verbose_name="Инвентарный объект") 
    
    qr = models.ImageField(upload_to='qr_codes/', 
                           verbose_name="QR-код")
    
    def ___str__(self):
        return f'QRcode'