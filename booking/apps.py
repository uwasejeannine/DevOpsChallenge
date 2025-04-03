from django.apps import AppConfig


class BookingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'booking'
    verbose_name = 'Booking'
    
    def ready(self):
        import booking.signals
        return True