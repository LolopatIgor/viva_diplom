from django import forms
from datetime import datetime, date, timedelta
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['date', 'time_from', 'time_to', 'guests_count']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'min': date.today().isoformat(),
                'max': (date.today() + timedelta(days=14)).isoformat(),
            }),
            'time_from': forms.Select(attrs={
                'class': 'form-select',
                'id': 'time-from'
            }),
            'time_to': forms.Select(attrs={
                'class': 'form-select',
                'id': 'time-to'
            }),
            'guests_count': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'step': 1,
            }),
        }

    def __init__(self, *args, **kwargs):
        self.table = kwargs.pop('table', None)
        super().__init__(*args, **kwargs)

        # Устанавливаем максимальное количество гостей на основе вместимости стола
        if self.table:
            self.fields['guests_count'].widget.attrs['max'] = self.table.capacity

    def clean_guests_count(self):
        guests = self.cleaned_data.get('guests_count')
        if guests is None:
            raise forms.ValidationError("Пожалуйста, укажите количество гостей.")
        if guests <= 0:
            raise forms.ValidationError("Количество гостей должно быть больше нуля.")
        if guests > self.table.capacity:
            raise forms.ValidationError(f"Количество гостей не может превышать вместимость стола ({self.table.capacity}).")
        return guests

    def clean(self):
        cleaned_data = super().clean()
        chosen_date = cleaned_data.get('date')
        time_from = cleaned_data.get('time_from')
        time_to = cleaned_data.get('time_to')
        guests_count = cleaned_data.get('guests_count')

        if not (chosen_date and time_from and time_to and guests_count):
            return cleaned_data

        # Проверка, что time_to > time_from
        if time_to <= time_from:
            self.add_error('time_to', "Время 'до' должно быть больше 'времени от'.")

        # Проверка, что разница не более 3 часов
        dt_from = datetime.combine(chosen_date, time_from)
        dt_to = datetime.combine(chosen_date, time_to)
        if (dt_to - dt_from) > timedelta(hours=3):
            self.add_error('time_to', "Разница между 'от' и 'до' не может превышать 3 часов.")

        # Проверка пересечений с другими заказами
        existing_bookings = Booking.objects.filter(table=self.table, date=chosen_date).exclude(pk=self.instance.pk)
        for b in existing_bookings:
            if not (time_to <= b.time_from or time_from >= b.time_to):
                # Есть пересечение
                self.add_error('time_from', "Выбранный интервал пересекается с уже существующей бронью.")
                break

        # Проверка количества гостей уже выполнена в clean_guests_count

        return cleaned_data
