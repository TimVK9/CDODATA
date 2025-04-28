from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image, ImageDraw, ImageFont
from .models import InventoryItem, QrCode
import qrcode
from io import BytesIO
from django.core.files import File
import logging
from django.db.models.signals import pre_save




logger = logging.getLogger(__name__)
    
@receiver(post_save, sender=InventoryItem)
def create_or_update_qrcode(sender, instance, created, **kwargs):
    # Генерация данных для QR-кода
    
    qr_data = f'https://github.com/TimVK9/D2/blob/main/news/templates/news{instance.get_absolute_url()}'
    print(f'Это даннные {qr_data}')

    
    # Создание QR-кода
    qr_img = qrcode.make(qr_data)
    draw = ImageDraw.Draw(qr_img)

    # Загрузка шрифта
    try:
        font = ImageFont.truetype("times new roman.ttf", 50)
    except IOError:
        font = ImageFont.load_default()


    # Позиция для текста
    text_position = (40, qr_img.size[1] - 30)

    # Добавление текста на изображение
    draw.text(text_position, f"Inv. No: {str(instance.inventory_number).zfill(12)}", font=font, fill="black")
    
    # Сохранение QR-кода в объект BytesIO
    qr_io = BytesIO()
    qr_img.save(qr_io, format='PNG')
    qr_file = File(qr_io, name=f"{instance.inventory_number}_qrcode.png")
    
    if created:
        # Создание объекта QrCode при создании InventoryItem
        QrCode.objects.create(objects_item=instance, qr=qr_file)

    else:
        # Обновление существующего объекта QrCode при изменении InventoryItem
        qr_code = QrCode.objects.get(objects_item=instance)
        qr_code.qr.save(f"{instance.inventory_number}_qrcode.png", qr_file)
        
        
