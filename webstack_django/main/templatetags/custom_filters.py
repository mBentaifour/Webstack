from django import template

register = template.Library()

@register.filter
def split(value, delimiter=','):
    """
    Divise une chaîne de caractères en liste selon un délimiteur.
    Usage: {{ value|split:"," }}
    """
    if value:
        return value.split(delimiter)
    return []
