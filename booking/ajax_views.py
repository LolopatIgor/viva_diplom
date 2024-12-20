# booking/ajax_views.py
from django.http import JsonResponse
from datetime import date, datetime, timedelta, time
from .models import Booking, Table
from django.views.decorators.http import require_GET


@require_GET
def get_available_from_times(request):
    table_id = request.GET.get('table_id')
    selected_date = request.GET.get('date')  # в формате YYYY-MM-DD

    if not table_id or not selected_date:
        return JsonResponse({'error': 'Missing parameters'}, status=400)

    table = Table.objects.get(pk=table_id)
    chosen_date = datetime.strptime(selected_date, '%Y-%m-%d').date()

    # Генерируем слоты 15 минут (пример: 09:00 - 23:00)
    start_time = time(9, 0)
    end_time = time(23, 0)

    time_slots = generate_time_slots(start_time, end_time, 15)

    # Фильтрация слотов по условию "не раньше, чем через 1 час от текущего времени"
    today = date.today()
    now = datetime.now()
    available_from_slots = time_slots[:]

    if chosen_date == today:
        one_hour_later = (now + timedelta(hours=1)).time()
        available_from_slots = [slot for slot in available_from_slots if slot >= one_hour_later]

    # Исключаем слоты, занятые другими бронями
    existing_bookings = Booking.objects.filter(table=table, date=chosen_date)
    occupied_slots = set()
    for b in existing_bookings:
        occupied_slots.update(generate_occupied_slots(b.time_from, b.time_to, 15))

    available_from_slots = [slot for slot in available_from_slots if slot not in occupied_slots]

    # Возвращаем в формате "HH:MM"
    slot_strings = [s.strftime("%H:%M") for s in available_from_slots]
    return JsonResponse({'slots': slot_strings})


@require_GET
def get_available_to_times(request):
    table_id = request.GET.get('table_id')
    selected_date = request.GET.get('date')
    time_from_str = request.GET.get('time_from')

    if not table_id or not selected_date or not time_from_str:
        return JsonResponse({'error': 'Missing parameters'}, status=400)

    table = Table.objects.get(pk=table_id)
    chosen_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    time_from = datetime.strptime(time_from_str, "%H:%M").time()

    # Аналогично генерируем все слоты
    start_time = time(9, 0)
    end_time = time(23, 0)
    time_slots = generate_time_slots(start_time, end_time, 15)

    # Фильтруем слоты для time_to:
    # - Должны быть > time_from
    # - Не больше 3 часов от time_from
    dt_from = datetime.combine(chosen_date, time_from)
    max_to_dt = dt_from + timedelta(hours=3)

    possible_to_slots = [t for t in time_slots if t > time_from and datetime.combine(chosen_date, t) <= max_to_dt]

    # Исключаем пересечения с уже существующими бронями
    existing_bookings = Booking.objects.filter(table=table, date=chosen_date)
    # Проверяем для каждого слота time_to, есть ли пересечение
    final_to_slots = []
    for candidate in possible_to_slots:
        # Интервал: time_from - candidate
        dt_candidate = datetime.combine(chosen_date, candidate)
        # Проверяем пересечения
        intersect = existing_bookings.filter(
            time_from__lt=candidate,
            time_to__gt=time_from
        ).exists()
        if not intersect:
            final_to_slots.append(candidate)

    slot_strings = [s.strftime("%H:%M") for s in final_to_slots]
    return JsonResponse({'slots': slot_strings})


def generate_time_slots(start, end, interval_minutes):
    slots = []
    current = datetime.combine(date.today(), start)
    end_dt = datetime.combine(date.today(), end)
    while current <= end_dt:
        slots.append(current.time())
        current += timedelta(minutes=interval_minutes)
    return slots


def generate_occupied_slots(start, end, interval):
    slots = []
    current = datetime.combine(date.today(), start)
    end_dt = datetime.combine(date.today(), end)
    while current < end_dt:
        slots.append(current.time())
        current += timedelta(minutes=interval)
    return slots

def get_table_capacity(request):
    table_id = request.GET.get('table_id')
    if not table_id:
        return JsonResponse({'error': 'Missing table_id parameter'}, status=400)
    try:
        table = Table.objects.get(pk=table_id)
        return JsonResponse({'capacity': table.capacity})
    except Table.DoesNotExist:
        return JsonResponse({'error': 'Table does not exist'}, status=404)
