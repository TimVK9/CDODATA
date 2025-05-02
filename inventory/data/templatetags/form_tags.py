from django import template
from django.forms.widgets import DateInput, Select

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    """Добавляет CSS класс к полю формы с учетом типа виджета"""
    if hasattr(field, 'as_widget'):
        widget = field.field.widget
        
        # Для полей даты устанавливаем тип date
        if isinstance(widget, DateInput):
            attrs = widget.attrs.copy()
            attrs.update({
                'class': f'{css_class} datepicker',
                'type': 'date'
            })
            return field.as_widget(attrs=attrs)
        
        # Для select устанавливаем form-select
        if isinstance(widget, Select):
            if 'form-control' in css_class:
                css_class = css_class.replace('form-control', 'form-select')
            elif 'form-select' not in css_class:
                css_class += ' form-select'
        
        return field.as_widget(attrs={'class': css_class})
    return field

@register.filter
def add_help_text(field):
    """Добавляет текст подсказки к полю"""
    if hasattr(field, 'field') and hasattr(field.field, 'help_text'):
        help_text = field.field.help_text
        if help_text:
            return f'<small class="form-text text-muted">{help_text}</small>'
    return ''