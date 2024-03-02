from django.db.models import Count
from rest_framework import serializers
from django.contrib.auth.models import User


from .models import Lesson, Product


class ProductSerializer(serializers.ModelSerializer):
    lesson_count = serializers.IntegerField(source='lesson_set.count', read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'start_date_time', 'price', 'lesson_count']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'video_link']


class ProductStatsSerializer(serializers.ModelSerializer):
    num_students = serializers.SerializerMethodField()
    group_fill_percentage = serializers.SerializerMethodField()
    purchase_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'num_students', 'group_fill_percentage', 'purchase_percentage']

    def get_group_fill_percentage(self, obj):
        total_groups = obj.group_set.count()
        if total_groups == 0:
            return 0
        else:
            filled_groups = obj.group_set.annotate(num_students=Count('students')).filter(
                num_students__gte=obj.min_students_per_group).count()
            return round((filled_groups / total_groups) * 100, 2)

    def get_num_students(self, obj):
        return obj.userproductaccess_set.count()

    def get_purchase_percentage(self, obj):
        total_users = User.objects.count()
        if total_users == 0:
            return 0
        else:
            purchased_products = obj.userproductaccess_set.count()
            return round((purchased_products / total_users) * 100, 2)