from django.utils import timezone
from django.db.models import Count
from .models import Group


def distribute_user_to_groups(user, product):
    if product.start_date_time <= timezone.now():
        groups = Group.objects.filter(product=product).annotate(num_students=Count('students')).order_by('num_students')
        min_students_per_group = product.min_students_per_group
        max_students_per_group = product.max_students_per_group

        for group in groups:
            if group.num_students < max_students_per_group:
                group.students.add(user)
                return group

        new_group = Group.objects.create(product=product, name=f"Group {groups.count() + 1}")
        new_group.students.add(user)
        return new_group

    else:
        groups = Group.objects.filter(product=product).annotate(num_students=Count('students')).order_by('num_students')
        min_students_per_group = product.min_students_per_group
        max_students_per_group = product.max_students_per_group

        min_group = groups.first()
        if min_group.num_students < min_students_per_group:
            min_group.students.add(user)
            return min_group

        max_group = groups.last()
        if max_group.num_students < max_students_per_group:
            max_group.students.add(user)
            return max_group

        new_group = Group.objects.create(product=product, name=f"Group {groups.count() + 1}")
        new_group.students.add(user)
        return new_group
