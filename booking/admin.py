from django.contrib import admin
from .models import Table, Booking

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'table_type')
    list_filter = ('table_type',)
    search_fields = ('name',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'table', 'date', 'time_from', 'time_to', 'is_confirmed')
    list_filter = ('is_confirmed', 'date', 'table')
    search_fields = ('user__email', 'table__name')