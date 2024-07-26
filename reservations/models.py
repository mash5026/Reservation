from django.db import models
from django_jalali.db import models as jmodels
from django.core.exceptions import ValidationError


class Table(models.Model):
    number = models.IntegerField(unique=True)
    name = models.CharField(max_length=30, null=True)
    capacity = models.IntegerField(null=True)
    location_x = models.IntegerField()  # X coordinate on the map
    location_y = models.IntegerField()  # Y coordinate on the map

    def __str__(self):
        return f"جدول {self.name}"

class Reservation(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    date = jmodels.jDateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    #user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('table', 'date', 'start_time', 'end_time')

    def clean(self):
        # Check if there is an overlapping reservation
        overlapping_reservations = Reservation.objects.filter(
            table=self.table,
            date=self.date,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time,
        ).exclude(id=self.id)

        if overlapping_reservations.exists():
            raise ValidationError("This reservation overlaps with another reservation.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Reservation for {self.table} on {self.date} from {self.start_time} to {self.end_time}"
    
    def get_date(self):
        return self.date.strftime('%Y/%m/%d')
    get_date.short_description = "تاریخ رزرو"