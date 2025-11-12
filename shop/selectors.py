from datetime import timedelta

from django.db.models import Sum
from django.db.models.query import QuerySet
from django.utils import timezone

from shop.models.order import OrderItem


def get_top_selling_products(days: int = 30, limit: int = 10) -> QuerySet[OrderItem]:
    """
    Retrieve the top selling products in the last 'days' days.

    Args:
        days (int): Number of days to look back for sales data.
        limit (int): Number of top products to return.

    Returns:
        QuerySet[OrderItem]: A queryset of top selling products with their total sold quantity.
    """
    since = timezone.now() - timedelta(days=days)
    top_sellers = (
        OrderItem.objects.filter(order__created_at__gte=since)
        .values("product__id", "product__name")
        .annotate(total_sold=Sum("quantity"))
        .order_by("-total_sold")[:limit]
    )
    return top_sellers
