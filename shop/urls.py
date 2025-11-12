from django.urls import path

from .views import TopSellerAPIView

urlpatterns = [
    path("top-sellers/", TopSellerAPIView.as_view()),
]
