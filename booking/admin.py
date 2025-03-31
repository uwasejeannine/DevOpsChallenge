from django.contrib import admin

from .models import Booking, FitnessClass, UserProfile


@admin.register(FitnessClass)
class FitnessClassAdmin(admin.ModelAdmin):
    list_display = ("name", "instructor", "date", "start_time", "end_time", "capacity")
    list_filter = ("date", "instructor")
    search_fields = ("name", "instructor", "description")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("user", "fitness_class", "booking_date")
    list_filter = ("booking_date", "fitness_class")
    search_fields = ("user__username", "fitness_class__name")


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone")
    search_fields = ("user__username", "user__email", "phone")
