from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('book', views.table_map, name='table_map'),
    path('table/<int:table_id>/', views.table_detail, name='table_detail'),
    path('table/<int:table_id>/reserve/', views.make_reservation, name='make_reservation'),
    path('calendar/', views.reservation_calendar, name='reservation_calendar'),
    path('api/reservations/', views.get_reservations, name='get_reservations'),


]