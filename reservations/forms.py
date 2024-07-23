from django import forms
from .models import Reservation
from django_jalali.forms import jDateField, jDateInput
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget

class ReservationForm(forms.ModelForm):

    #date = jDateField(widget=jDateInput(attrs={'class':'jalali_date'}))

    class Meta:
        model = Reservation
        fields = ['table', 'date', 'start_time', 'end_time']
        widgets = {
            #'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
            super(ReservationForm, self).__init__(*args, **kwargs)
            self.fields['date'] = JalaliDateField(label=('تاریخ'), 
                widget=AdminJalaliDateWidget
            )

            # you can added a "class" to this field for use your datepicker!
            # self.fields['date'].widget.attrs.update({'class': 'jalali_date-date'})