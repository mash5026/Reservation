from django import forms
from .models import Reservation
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget
from django.core.exceptions import ValidationError

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
        self.fields['date'] = JalaliDateField(
            label='تاریخ',
            widget=AdminJalaliDateWidget(attrs={'class': 'jalali_date-date'}),
            error_messages={
                'required': 'لطفاً تاریخ را وارد کنید',
                'invalid': 'تاریخ وارد شده معتبر نیست'
            }
        )
        self.fields['table'].error_messages.update({
            'required': 'لطفاً میز را انتخاب کنید',
        })
        self.fields['start_time'].error_messages.update({
            'required': 'لطفاً زمان شروع را وارد کنید',
            'invalid': 'زمان شروع معتبر نیست'
        })
        self.fields['end_time'].error_messages.update({
            'required': 'لطفاً زمان پایان را وارد کنید',
            'invalid': 'زمان پایان معتبر نیست'
        })

    def clean(self):
        cleaned_data = super().clean()
        table = cleaned_data.get('table')
        date = cleaned_data.get('date')
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if table and date and start_time and end_time:
            existing_reservations = Reservation.objects.filter(
                table=table,
                date=date,
                start_time__lt=end_time,
                end_time__gt=start_time
            )
            if existing_reservations.exists():
                self.add_error(None, 'ظرفیت میز انتخابی در ساعت و تاریخ مد نظر شما پر می باشد')
