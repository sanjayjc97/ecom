from django import template
from django.db.models import F,Aggregate,Sum

register = template.Library()


@register.filter
def get_count(listing):
    return listing.aggregate(total_quantity = Sum('quantity')).get('total_quantity')




@register.filter
def get_total_price(listing):
    return listing.aggregate(total_price = Sum('price')).get('total_price')