from rest_framework import serializers


class TopSellerSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(source="product__id")
    product_name = serializers.CharField(source="product__name")
    total_sold = serializers.IntegerField()
