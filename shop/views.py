from django.conf import settings
from django.core.cache import cache
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from shop.selectors import get_top_selling_products
from shop.serializers import TopSellerSerializer


class TopSellerAPIView(APIView):
    def get(self, request: Request) -> Response:
        cache_key = "top_selling_products"
        cached_data = cache.get(cache_key)
        if cached_data:
            print("Top selling products fetched from cache.")
            return Response(cached_data, status=status.HTTP_200_OK)

        queryset = get_top_selling_products(days=30, limit=10)
        serializer = TopSellerSerializer(queryset, many=True)
        print("Top selling products fetched from database and serialized.")
        cache.set(cache_key, serializer.data, timeout=settings.CACHE_TIMEOUT)

        return Response(serializer.data, status=status.HTTP_200_OK)
