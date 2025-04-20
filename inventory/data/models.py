from django.db import models

class Base(models.Model):
    name = models.CharField(max_length=64, verbose_name="Название подразделения")
    address = models.CharField(max_length=255, verbose_name="Адрес подразделения")

    def __str__(self):
        return f"{self.name} - {self.address}"
    
    class Meta:
        verbose_name = "Подразделение"
        verbose_name_plural = "Подразделения"
    
    
    
class InventoryItem(models.Model):
    
    name = models.CharField(max_length=128, null=False, verbose_name="Инвентаризационный объект")
    inventory_number = models.CharField(max_length=50, unique=True, null=False, verbose_name="Инвентаризационный номер")
    value = models.DecimalField(max_digits=10, decimal_places=2, null=False, verbose_name="Балансовая стоимость") 
    base = models.ForeignKey(Base, on_delete=models.CASCADE, null=False, verbose_name="Подразделение")
    office = models.SmallIntegerField(null=False, verbose_name="Кабинет расположения")
    user_name = models.CharField(max_length=255, default='Ответсвенный за содержание', null=False, verbose_name='Отвественный за содержание')
    
    def __str__(self):
        return f'''
                   {self.name};\n
                   Инвентаризационный номер - {self.inventory_number};\n
                   Балансовая стоимость - {self.value};\n
                   База - {self.base};\n
                   Кабинет размещения - {self.office};\n
                   Ответсвенный за содержание - {self.user_name};\n
                   
                '''
    class Meta:
        
        verbose_name = "Инвентаризационные данные"
        verbose_name_plural = "Инвентаризационные данные"
        
        
        
class QrCode(models.Model):
    objects_item = models.OneToOneField(InventoryItem, on_delete=models.CASCADE, verbose_name="Инвентарный объект") 
    qr = models.ImageField(upload_to='qr_codes/', verbose_name="QR-код")
    
    def ___str__(self):
        return f'QRcode'