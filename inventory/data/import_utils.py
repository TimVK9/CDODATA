import pandas as pd
from datetime import datetime, date
from django.core.exceptions import ValidationError
from .models import BaseInfo, InventoryItem
import os


def import_inventory_from_excel(file_path):
    """
    Импортирует данные инвентаризации из Excel файла
    с автоматическим преобразованием длинных названий счетов в коды
    """
    try:
        # ===== 1. ЧТЕНИЕ ФАЙЛА =====
        try:
            df = pd.read_excel(
                file_path,
                parse_dates=['Дата ввода'],
                dtype={'Инвентарный номер* (12 цифр)': str}
            )
        except Exception as e:
            raise ValueError(f"Ошибка чтения файла Excel: {str(e)}")

        # ===== 2. ПРОВЕРКА ДАННЫХ =====
        required_columns = [
            'Подразделение',
            'Инвентарный номер* (12 цифр)',
            'Наименование объекта',
            'Счет актива'
        ]
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise ValueError(f"Отсутствуют обязательные колонки: {', '.join(missing_columns)}")

        # Очистка пустых значений
        df = df.where(pd.notnull(df), None)
        
        # Преобразование даты
        if 'Дата ввода' in df.columns:
            df['Дата ввода'] = pd.to_datetime(df['Дата ввода'], errors='coerce').dt.date

        # ===== 3. ПОДГОТОВКА ФУНКЦИИ ПРЕОБРАЗОВАНИЯ =====
        def get_value_code(full_value):
            """Преобразует полное название счета в короткий код"""
            if not full_value or not isinstance(full_value, str):
                return '101.34.00.00'
            
            value_mapping = {
                '101.12': '101.12.00.00',
                '103.11': '103.11.00.00',
                '101.22': '101.22.00.00',
                '101.24': '101.24.00.00',
                '101.34': '101.34.00.00',
                '21.34': '21.34.00.00',
                '101.36': '101.36.00.00',
                '21.36': '21.36.00.00',
            }
            
            # Извлекаем числовой префикс
            prefix = full_value.split(',')[0].strip().split()[0].strip()
            
            # Ищем соответствие
            for key in value_mapping:
                if prefix.startswith(key):
                    return value_mapping[key]
            
            return '101.34.00.00'

        # ===== 4. ОБРАБОТКА КАЖДОЙ СТРОКИ =====
        base_cache = {}
        result = {
            'created': 0,
            'updated': 0,
            'errors': [],
            'total': len(df),
            'warnings': []
        }

        for index, row in df.iterrows():
            try:
                # ---- 4.1 Обработка подразделения ----
                base_name = str(row['Подразделение']).strip()
                if not base_name:
                    raise ValueError("Отсутствует подразделение")
                
                if base_name not in base_cache:
                    base, created = BaseInfo.objects.get_or_create(
                        base_name=base_name,
                        defaults={'base_address': f"Автоматически созданный адрес для {base_name}"}
                    )
                    base_cache[base_name] = base

                # ---- 4.2 Обработка инвентарного номера ----
                inv_number = str(row['Инвентарный номер* (12 цифр)'] or '').strip()
                inv_number = inv_number.zfill(12)[:12]

                # ---- 4.3 Обработка счета актива ----
                account_value = str(row.get('Счет актива', '')).strip()
                value_code = get_value_code(account_value)
                
                # Логируем нестандартные счета
                if value_code == '101.34.00.00' and account_value:
                    result['warnings'].append(
                        f"Строка {index+2}: Использовано значение по умолчанию для счета: '{account_value}'"
                    )

                # ---- 4.4 Подготовка данных ----
                defaults = {
                    'objects_name': str(row['Наименование объекта'] or 'Не указано').strip(),
                    'state': str(row.get('Состояние', '') or 'Введено в эксплуатацию').strip(),
                    'value': value_code,  # Используем преобразованный код
                    'base': base_cache[base_name],
                    'office': str(row.get('Кабинет', '') or '0').strip(),
                    'accountable_user': str(row.get('Ответственный за содержание', '') or 'Ответственный не указан').strip(),
                    'start_date': row.get('Дата ввода') or date.today(),
                    'description': str(row.get('Описание', '') or 'Описание отсутствует').strip(),
                }

                # ---- 4.5 Сохранение данных ----
                obj, created = InventoryItem.objects.update_or_create(
                    inventory_number=inv_number,
                    defaults=defaults
                )
                
                if created:
                    result['created'] += 1
                else:
                    result['updated'] += 1

            except Exception as e:
                result['errors'].append(f"Строка {index + 2}: {str(e)}")
                continue

        return result

    except Exception as e:
        raise ValueError(f"Ошибка при обработке файла: {str(e)}")