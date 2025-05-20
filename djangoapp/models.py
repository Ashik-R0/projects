from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tourpakage(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField(blank=True,null=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    duration=models.CharField(max_length=100)
    image  =models.ImageField(upload_to='packages/')
    trending = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255,default='Unknown')
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='packages',null=True) 
    is_approved = models.BooleanField(default=False)


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('vendor', 'Vendor'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.email} - {self.role}"

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    tour = models.ForeignKey(Tourpakage, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    number_of_people = models.IntegerField()
    status = models.CharField(max_length=20, default='Pending') 

