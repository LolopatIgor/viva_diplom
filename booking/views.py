from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from datetime import date, timedelta, datetime

from .decorators import manager_required
from .models import Table, Booking
from .forms import BookingForm

def book_table(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    if request.method == 'POST':
        form = BookingForm(request.POST, table=table)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.table = table
            booking.save()
            return redirect('booking:booking_list')
    else:
        form = BookingForm(table=table)

    return render(request, 'booking/book_table.html', {'table': table, 'form': form})


@login_required
def booking_list(request):
    tables = Table.objects.all()
    return render(request, 'booking/booking_plan.html', {'tables': tables})


@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    # Комбинируем дату и время начала бронирования
    booking_datetime = datetime.combine(booking.date, booking.time_from)

    # Делаем booking_datetime осведомлённым о часовом поясе
    booking_datetime = timezone.make_aware(booking_datetime, timezone.get_current_timezone())

    # Проверяем, не началось ли бронирование
    if booking_datetime <= timezone.now():
        messages.error(request, "Невозможно отменить бронь, время уже наступило.")
    else:
        booking.delete()
        messages.success(request, "Бронирование успешно отменено.")

    return redirect('booking:user_profile')


@login_required
def user_profile(request):
    now = timezone.now()

    # Получаем текущие (предстоящие) бронирования пользователя
    current_bookings = Booking.objects.filter(
        user=request.user
    ).filter(
        Q(date__gt=now.date()) |
        Q(date=now.date(), time_from__gt=now.time())
    ).order_by('date', 'time_from')

    # Получаем прошлые бронирования пользователя
    past_bookings = Booking.objects.filter(
        user=request.user
    ).filter(
        Q(date__lt=now.date()) |
        Q(date=now.date(), time_from__lte=now.time())
    ).order_by('-date', '-time_from')

    return render(request, 'booking/user_profile.html', {
        'current_bookings': current_bookings,
        'past_bookings': past_bookings
    })

@manager_required(login_url='users')  # Убедитесь, что маршрут 'login' существует
def manager_dashboard(request):
    now = timezone.now()

    # Все утвержденные бронирования, которые еще не прошли
    approved_bookings = Booking.objects.filter(
        is_confirmed=True
    ).filter(
        Q(date__gt=now.date()) |
        Q(date=now.date(), time_from__gt=now.time())
    ).order_by('date', 'time_from')

    # Все бронирования, которые нужно утвердить или отклонить
    pending_bookings = Booking.objects.filter(
        is_confirmed=False
    ).filter(
        Q(date__gte=now.date())
    ).order_by('date', 'time_from')

    return render(request, 'booking/manager_dashboard.html', {
        'approved_bookings': approved_bookings,
        'pending_bookings': pending_bookings,
    })

@manager_required(login_url='users')
def confirm_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        booking.is_confirmed = True
        booking.save()
        messages.success(request, f"Бронирование на стол '{booking.table.name}' подтверждено.")
        return redirect('booking:manager_dashboard')

    return render(request, 'booking/confirm_booking.html', {'booking': booking})

@manager_required(login_url='users')
def reject_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == 'POST':
        booking.delete()
        messages.success(request, f"Бронирование на стол '{booking.table.name}' отклонено.")
        return redirect('booking:manager_dashboard')

    return render(request, 'booking/reject_booking.html', {'booking': booking})