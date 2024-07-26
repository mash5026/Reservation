from django import forms
from .models import Reservation
from django_jalali.forms import jDateField, jDateInput
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['table', 'date', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }
        labels = {
            'table': 'میز',
            'date': 'تاریخ',
            'start_time': 'زمان شروع',
            'end_time': 'زمان پایان',
        }

    def __init__(self, *args, **kwargs):
        super(ReservationForm, self).__init__(*args, **kwargs)
        self.fields['date'] = JalaliDateField(label=('تاریخ'),
            widget=AdminJalaliDateWidget(attrs={'class': 'jalali_date-date'})
        )
