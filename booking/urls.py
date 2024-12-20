from django.urls import path
from . import views
from . import ajax_views

app_name = 'booking'

urlpatterns = [
    path('', views.booking_list, name='booking_list'),
    path('profile/', views.user_profile, name='user_profile'),
    path('manager/', views.manager_dashboard, name='manager_dashboard'),  # Маршрут для менеджера
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('confirm/<int:booking_id>/', views.confirm_booking, name='confirm_booking'),  # Маршрут подтверждения
    path('reject/<int:booking_id>/', views.reject_booking, name='reject_booking'),        # Маршрут отклонения
    path('table/<int:table_id>/', views.book_table, name='book_table'),
    path('ajax/get_from_times/', ajax_views.get_available_from_times, name='get_from_times'),
    path('ajax/get_to_times/', ajax_views.get_available_to_times, name='get_to_times'),
    path('ajax/get_table_capacity/', ajax_views.get_table_capacity, name='get_table_capacity'),
]
