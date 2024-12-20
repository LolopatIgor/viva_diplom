# booking/management/commands/create_initial_users.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from booking.models import Booking
from users.models import User


class Command(BaseCommand):
    help = 'Создает начальных пользователей и группу Manager с необходимыми правами.'

    def handle(self, *args, **options):
        # Определяем данные пользователей
        users_data = [
            {
                'email': 'admin@gmail.com',
                'first_name': 'Admin',
                'last_name': 'Viva',
                'phone': '+7777777',
                'is_staff': True,
                'is_superuser': True,
                'password': '123',
                'group': None
            },
            {
                'email': 'manager@gmail.com',
                'first_name': 'Manager',
                'last_name': 'Viva',
                'phone': '+7777777',
                'is_staff': True,
                'is_superuser': False,
                'password': '123',
                'group': 'Manager'
            },
            {
                'email': 'user@gmail.com',
                'first_name': 'User',
                'last_name': 'Viva',
                'phone': '+7777777',
                'is_staff': False,
                'is_superuser': False,
                'password': '123',
                'group': None  # Обычный пользователь не назначается в группу Manager
            },
        ]

        # Создаем или получаем группу Manager
        group, created = Group.objects.get_or_create(name='Manager')
        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Manager" успешно создана.'))
        else:
            self.stdout.write('Группа "Manager" уже существует.')

        # Получаем контент-тайп для модели Booking
        booking_ct = ContentType.objects.get_for_model(Booking)

        # Получаем необходимые права
        permissions = Permission.objects.filter(
            content_type=booking_ct,
            codename__in=['change_booking', 'view_booking']
        )

        # Назначаем права группе Manager
        if permissions.exists():
            group.permissions.set(permissions)
            self.stdout.write(self.style.SUCCESS('Права "change_booking" и "view_booking" добавлены в группу "Manager".'))
        else:
            self.stdout.write(self.style.WARNING('Не найдены необходимые права для модели Booking.'))

        # Создаем или получаем пользователей
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                email=user_data['email'],
                defaults={
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'phone': user_data['phone'],
                    'is_staff': user_data['is_staff'],
                    'is_superuser': user_data['is_superuser'],
                }
            )

            if created:
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Пользователь "{user.email}" успешно создан.'))
            else:
                self.stdout.write(f'Пользователь "{user.email}" уже существует.')

            # Назначаем пользователя в группу, если указано
            if user_data['group']:
                try:
                    target_group = Group.objects.get(name=user_data['group'])
                    user.groups.add(target_group)
                    self.stdout.write(self.style.SUCCESS(f'Пользователь "{user.email}" добавлен в группу "{user_data["group"]}".'))
                except Group.DoesNotExist:
                    self.stdout.write(self.style.ERROR(f'Группа "{user_data["group"]}" не найдена. Пользователь "{user.email}" не добавлен в группу.'))
