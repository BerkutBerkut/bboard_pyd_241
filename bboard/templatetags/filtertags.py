from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# фильтр
@register.filter(name='cur')
def currency(value, name='тг.'):
    return f'{value:.2f} {name}'

# register.filter('currency', currency)


# тэги
@register.simple_tag
def lst(sep, *args):
    return mark_safe(f"{sep.join(args)} (итого: <strong>{len(args)}</strong>)")

# тэги на основе шаблона
@register.inclusion_tag('tags/ulist.html')
def ulist(*args):
    return {'items': args}