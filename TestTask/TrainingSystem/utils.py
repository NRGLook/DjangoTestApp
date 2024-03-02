from django.utils import timezone
from .models import Group


def distribute_user_to_groups(user, product):
    if product.start_date_time <= timezone.now():  # Если продукт уже начался
        groups = Group.objects.filter(product=product).order_by('students__count')
        min_students_per_group = product.min_students_per_group
        max_students_per_group = product.max_students_per_group

        for group in groups:
            if group.students.count() < max_students_per_group:
                group.students.add(user)
                return group

        new_group = Group.objects.create(product=product, name=f"Group {groups.count() + 1}")
        new_group.students.add(user)
        return new_group

    else:
        temporary_group, created = Group.objects.get_or_create(
            product=product,
            name=f"Temporary Group for {product.name}"
        )
        temporary_group.students.add(user)
        return temporary_group
