from django.core.exceptions import ValidationError

def validate_description_length(value):
    if len(value) < 100:
        raise ValidationError('Описание не должно быть короче 10 символов')
