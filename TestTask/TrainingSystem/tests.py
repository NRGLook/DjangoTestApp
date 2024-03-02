from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from .models import Product, Lesson


class ProductListAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('product-list')
        self.product1 = Product.objects.create(name='Product 1', start_date_time='2024-01-01', price=10)
        self.product2 = Product.objects.create(name='Product 2', start_date_time='2024-01-02', price=20)

    def test_product_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 2)


class LessonListAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.product = Product.objects.create(name='Test Product')
        self.lesson1 = Lesson.objects.create(title='Lesson 1', product=self.product)
        self.lesson2 = Lesson.objects.create(title='Lesson 2', product=self.product)
        self.url = reverse('lesson-list', kwargs={'product_id': self.product.id})

    def test_lesson_list_authenticated_user(self):
        self.client.force_login(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


class ProductStatsAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('product-stats')
        self.product = Product.objects.create(name='Product', start_date_time='2024-01-01', price=10)

    def test_product_stats(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
