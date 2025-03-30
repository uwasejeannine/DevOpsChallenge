from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('booking.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='booking/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(
        template_name='booking/logout.html',
        next_page='home'
    ), name='logout'),
]

# Add static and media URL patterns in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)