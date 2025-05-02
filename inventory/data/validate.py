from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_description_length(value):
    if len(value) < 10:
        raise ValidationError('Описание не должно быть короче 10 символов')


def validate_number_int(value):
    if not value.isdigit():
        raise ValidationError('Инвентарный номер должен состоять из цифрр')
    
    
def validate_date_not_in_future(value):
    if value > timezone.now().date():
        raise ValidationError("Дата не может быть в будущем")