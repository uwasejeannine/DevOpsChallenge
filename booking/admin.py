from django.contrib import admin

from .models import Booking, FitnessClass, UserProfile


@admin.register(FitnessClass)
class FitnessClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'instructor', 'date', 'start_time', 'end_time', 'capacity', 'category']
    search_fields = ['name', 'instructor', 'category']
    list_filter = ['date', 'category']
    
    def get_ordering(self, request):
        return ['-date', 'start_time']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'fitness_class', 'created_at']
    search_fields = ['user__username', 'fitness_class__name']
    list_filter = ['created_at']
    
    def get_readonly_fields(self, request, obj=None):
        return ['created_at'] if obj else []


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone']
    search_fields = ['user__username', 'phone']
    
    def get_fieldsets(self, request, obj=None):
        return [(None, {'fields': ['user', 'phone', 'bio', 'preferred_categories']})]