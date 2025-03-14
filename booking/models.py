from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class FitnessClass(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    instructor = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    capacity = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.name} - {self.date} {self.start_time}"
    
    @property
    def is_full(self):
        return self.booking_set.count() >= self.capacity

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return self.user.username

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('user', 'fitness_class')
        
    def __str__(self):
        return f"{self.user.username} - {self.fitness_class.name}"