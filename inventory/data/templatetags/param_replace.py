from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """
    Тег для сохранения параметров URL при пагинации
    Использование: {% param_replace page=2 %}
    """
    request = context['request']
    params = request.GET.copy()
    for k, v in kwargs.items():
        params[k] = v
    return params.urlencode()