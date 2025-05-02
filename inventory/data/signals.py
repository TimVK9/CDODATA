# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.files import File
from PIL import Image, ImageDraw, ImageFont
import qrcode
import os
from io import BytesIO
import logging
from .models import InventoryItem, QrCode

logger = logging.getLogger(__name__)

@receiver(post_save, sender=InventoryItem)
def create_or_update_qrcode(sender, instance, created, **kwargs):
    """
    Создает или обновляет QR-код для инвентарного объекта.
    QR-код содержит ссылку на объект и инвентарный номер.
    """
    try:
        # Проверяем наличие обязательных данных
        if not instance.inventory_number:
            logger.warning(f"Пропуск генерации QR-кода: отсутствует инвентарный номер для объекта {instance.pk}")
            return

        # Генерация данных для QR-кода (используем абсолютный URL)
        qr_data = f"{settings.BASE_URL}{instance.get_absolute_url()}"
        logger.debug(f"Генерация QR-кода для {instance.inventory_number}: {qr_data}")

        # Создание QR-кода с улучшенными параметрами
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Создаем изображение
        qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
        draw = ImageDraw.Draw(qr_img)

        # Загрузка шрифта
        try:
            font_path = os.path.join(settings.BASE_DIR, 'static', 'fonts', 'Roboto-Regular.ttf')
            font = ImageFont.truetype(font_path, 20)
        except (IOError, OSError):
            font = ImageFont.load_default()
            logger.warning("Не удалось загрузить шрифт, используется стандартный")

        # Добавление текста с инвентарным номером
        text = f"Инв. №: {instance.inventory_number}"
        
        # Расчет размера и позиции текста
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        img_width, img_height = qr_img.size
        text_x = (img_width - text_width) // 2
        text_y = img_height - text_height - 15
        
        # Рисуем подложку и текст
        draw.rectangle(
            [text_x - 5, text_y - 5, text_x + text_width + 5, text_y + text_height + 5],
            fill="white"
        )
        draw.text((text_x, text_y), text, font=font, fill="black")

        # Сохранение изображения
        buffer = BytesIO()
        qr_img.save(buffer, format="PNG")
        
        # Создание или обновление QR-кода
        qr_file = File(buffer, name=f"qr_{instance.inventory_number}.png")
        
        if created:
            QrCode.objects.create(objects_item=instance, qr=qr_file)
            logger.info(f"Создан QR-код для инвентарного № {instance.inventory_number}")
        else:
            qr_code, created = QrCode.objects.get_or_create(objects_item=instance)
            qr_code.qr.save(f"qr_{instance.inventory_number}.png", qr_file, save=True)
            logger.info(f"Обновлен QR-код для инвентарного № {instance.inventory_number}")

    except Exception as e:
        logger.error(f"Ошибка при создании QR-кода: {str(e)}", exc_info=True)

