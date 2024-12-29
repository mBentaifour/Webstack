from django import template

register = template.Library()

@register.filter
def split(value, delimiter=','):
    """
    Divise une chaîne de caractères en liste selon un délimiteur.
    Exemple d'utilisation : {{ "1,2,3"|split:"," }}
    """
    if not value:
        return []
    return value.split(delimiter)
