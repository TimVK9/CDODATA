import pandas as pd
from datetime import datetime
from django.core.exceptions import ValidationError
from .models import BaseInfo, InventoryItem

def import_inventory_from_excel(file_path):
    # Чтение Excel файла
    df = pd.read_excel(file_path)
    
    # Замена NaN и пустых строк на None
    df = df.replace({pd.NA: None, '': None})
    
    # Словарь для сопоставления названий подразделений с объектами BaseInfo
    base_cache = {}
    
    # Счетчики для статистики
    created_count = 0
    updated_count = 0
    errors = []
    
    for index, row in df.iterrows():
        try:
            # Обработка подразделения (обязательное поле)
            base_name = row['Подразделение']
            if not base_name:
                errors.append(f"Строка {index + 2}: Отсутствует подразделение")
                continue
                
            if base_name not in base_cache:
                base, created = BaseInfo.objects.get_or_create(
                    base_name=base_name.strip(),
                    defaults={'base_address': f"Адрес для {base_name}"}
                )
                base_cache[base_name] = base
            
            # Обработка инвентарного номера - используем 12 нулей если нет значения
            inv_number = str(row['Инвентарный номер* (12 цифр)']) if row['Инвентарный номер* (12 цифр)'] else '000000000000'
            inv_number = inv_number.zfill(12)
            
            # Обработка даты (может быть пустой)
            start_date = row['Дата ввода']
            if isinstance(start_date, str):
                try:
                    start_date = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S').date()
                except ValueError:
                    start_date = None
            elif pd.isna(start_date):
                start_date = None
            
            # Обработка остальных полей с подстановкой значений по умолчанию
            defaults = {
                'objects_name': row['Наименование объекта'] or 'Не указано',
                'state': row['Состояние'] or 'Введено в эксплуатацию',
                'value': row['Счет актива'] or '101.34, Машины и оборудование – иное движимое имущество учреждения',
                'base': base_cache[base_name],
                'office': str(row['Кабинет']) if row['Кабинет'] not in [None, ''] else '0',
                'accountable_user': row['Ответственный за содержание'] or 'Ответственный не указан',
                'start_date': start_date or datetime.now().date(),
                'description': row['Описание'] or '''Здесь должно быть описание объекта, позволяющее легко его идентифицировать.
                    Здесь могут быть его характеристики, цвет, объем, системные данные и т.п.''',
            }
            
            # Получаем или создаем инвентарный объект
            obj, created = InventoryItem.objects.update_or_create(
                inventory_number=inv_number,
                defaults=defaults
            )
            
            if created:
                created_count += 1
            else:
                updated_count += 1
                
        except Exception as e:
            errors.append(f"Строка {index + 2}: Ошибка - {str(e)}")
            continue
    
    return {
        'created': created_count,
        'updated': updated_count,
        'errors': errors,
        'total': len(df),
    }