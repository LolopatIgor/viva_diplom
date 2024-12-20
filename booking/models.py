# booking/models.py
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class Table(models.Model):
    TABLE_TYPE_CHOICES = [
        ('regular', 'Обычный'),
        ('vip', 'VIP'),
        ('outdoor', 'На улице'),
    ]

    name = models.CharField(max_length=100, verbose_name='Имя столика')
    capacity = models.PositiveIntegerField(verbose_name='Количество человек')
    table_type = models.CharField(
        max_length=20,
        choices=TABLE_TYPE_CHOICES,
        verbose_name='Тип столика'
    )
    x_coord = models.PositiveIntegerField(verbose_name='X-позиция', default=0)
    y_coord = models.PositiveIntegerField(verbose_name='Y-позиция', default=0)

    def __str__(self):
        return f"{self.name} ({self.get_table_type_display()})"


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь')
    table = models.ForeignKey(Table, on_delete=models.CASCADE, verbose_name='Столик')
    date = models.DateField(verbose_name='Дата')
    time_from = models.TimeField(verbose_name='Время от')
    time_to = models.TimeField(verbose_name='Время до')
    guests_count = models.IntegerField(verbose_name='Количество гостей', default=1)
    is_confirmed = models.BooleanField(default=False, verbose_name='Подтвержден ли заказ')

    def __str__(self):
        return f"Бронирование от {self.user.email} на {self.date} стол: {self.table}"
