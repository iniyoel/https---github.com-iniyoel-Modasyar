from django import template

register = template.Library()

@register.filter
def currency_format(value):
    try:
        value = int(value)
        return f'{value:,.0f}'.replace(',', '.')
    except (ValueError, TypeError):
        return value
