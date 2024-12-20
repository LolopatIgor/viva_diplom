from django import template

register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
    """
    Проверяет, принадлежит ли пользователь к заданной группе.
    Использование в шаблоне: {% if user|has_group:"Manager" %}
    """
    return user.groups.filter(name=group_name).exists()
