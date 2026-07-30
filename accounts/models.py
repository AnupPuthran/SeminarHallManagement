from django.db import models
from django.contrib.auth.models import User


class SeminarHall(models.Model):
    hall_name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    location = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='hall_images/', blank=True, null=True)

    def __str__(self):
        return self.hall_name


class Booking(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hall = models.ForeignKey(SeminarHall, on_delete=models.CASCADE)
    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    def __str__(self):
        return f"{self.user.username} - {self.hall.hall_name}"