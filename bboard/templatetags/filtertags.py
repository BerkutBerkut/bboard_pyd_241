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

# функция обрезания строки
@register.filter
def cut_half(value):
    if isinstance(value, str):
        return value[:len(value)//2]
    return value

#  Функция разделяет строку по указанному сепаратору и возвращает массив
@register.simple_tag
def split_string(string, separator):
    if isinstance(string, str):
        return string.split(separator)
    return []

# Преобразование строки в нижний регистр
@register.filter
def to_lower(value):
    if isinstance(value, str):
        return value.lower()
    return value

# Удаление пробелов в строке
@register.filter
def delete_space(value):
    if isinstance(value, str):
        return value.replace(" ", "")
    return value

