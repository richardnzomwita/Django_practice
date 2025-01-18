# templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def multiply(value, arg):
    try:
        return value * arg
    except TypeError:
        return ''   

@register.filter
def sum_total_price(articles):
    """
    Calcule le total des prix des articles dans le panier.
    """
    return sum(article.quantite * article.produit.prix_unitaire for article in articles)

