from django.urls import path
from .views import ProductListAPIView, LessonListAPIView, ProductStatsAPIView


urlpatterns = [
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/<int:product_id>/lessons/', LessonListAPIView.as_view(), name='lesson-list'),
    path('products/stats/', ProductStatsAPIView.as_view(), name='product-stats'),
]
