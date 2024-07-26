from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.exceptions import ValidationError
from .models import Table, Reservation
from .forms import ReservationForm

def home(request):
    return render(request, 'reservations/home.html')
    
def table_map(request):
    tables = Table.objects.all()
    return render(request, 'reservations/table_map.html', {'tables': tables})

def table_detail(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    reservations = Reservation.objects.filter(table=table)
    return render(request, 'reservations/table_detail.html', {'table': table, 'reservations': reservations})

def make_reservation(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            try:
                reservation = form.save(commit=False)
                reservation.table = table
                reservation.user = request.user
                reservation.save()
                return redirect('table_detail', table_id=table.id)
            except ValidationError as e:
                form.add_error(None, e)
    else:
        form = ReservationForm()
    return render(request, 'reservations/make_reservation.html', {'form': form, 'table': table})

def reservation_calendar(request):
    tables = Table.objects.all()
    return render(request, 'reservations/reservation_calendar.html', {'tables': tables})

def get_reservations(request):
    reservations = Reservation.objects.all()
    events = []
    for reservation in reservations:
        event = {
            'title': f'Table {reservation.table.number}',
            'start': f'{reservation.date}T{reservation.start_time}',
            'end': f'{reservation.date}T{reservation.end_time}',
            'id': reservation.id,
        }
        events.append(event)
    return JsonResponse(events, safe=False)