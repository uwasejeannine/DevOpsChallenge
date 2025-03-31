from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class FitnessClass(models.Model):
    CATEGORY_CHOICES = [
        ("yoga", "Yoga"),
        ("hiit", "HIIT"),
        ("pilates", "Pilates"),
        ("spinning", "Spinning"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    instructor = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    capacity = models.IntegerField()
    category = models.CharField(max_length=50, default='general')

    # Your existing methods remain the same

    def __str__(self):
        return f"{self.name} - {self.date} {self.start_time}"

    @property
    def available_spots(self):
        booked_spots = self.booking_set.count()
        return self.capacity - booked_spots

    @property
    def is_full(self):
        return self.available_spots <= 0


class UserProfile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="userprofile"
    )
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)  # Optional bio
    preferred_categories = models.CharField(max_length=200, blank=True)

    def get_preferred_categories(self):
        if not self.preferred_categories:
            return []
        return [cat.strip() for cat in self.preferred_categories.split(',')]

    def __str__(self):
        return self.user.username

    class Meta:
        # Add explicit constraints
        constraints = [
            models.UniqueConstraint(fields=["user"], name="unique_user_profile")
        ]


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "fitness_class")

    def __str__(self):
        return f"{self.user.username} - {self.fitness_class.name}"
