from django.contrib import admin
from django_jalali.admin.filters import JDateFieldListFilter
from .models import Table, Reservation

class ReservationAdmin(admin.ModelAdmin):
    list_display = ['table', 'get_date' ,'start_time', 'end_time', 'user']
    list_filter = (
        ('date', JDateFieldListFilter),
    )

admin.site.register(Table)
admin.site.register(Reservation, ReservationAdmin)
