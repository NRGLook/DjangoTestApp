from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db.models import Count

from .models import Product, Lesson
from .serializers import LessonSerializer, ProductSerializer, ProductStatsSerializer

from django.http import HttpResponse
from django.views import View


class IndexView(View):
    def get(self, request):
        return HttpResponse("Welcome to our training system!")


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.prefetch_related('lesson_set')
    serializer_class = ProductSerializer


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Lesson.objects.filter(product_id=product_id)


class ProductStatsAPIView(APIView):
    def get(self, request, format=None):
        queryset = Product.objects.annotate(num_students=Count('userproductaccess')).all()
        serializer = ProductStatsSerializer(queryset, many=True)
        return Response(serializer.data)
