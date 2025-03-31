from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("classes/", views.classes, name="classes"),
    path("book-class/<int:class_id>/", views.book_class, name="book_class"),
    path(
        "cancel-booking/<int:booking_id>/", views.cancel_booking, name="cancel_booking"
    ),
    path(
        "booking-confirmation/<int:booking_id>/",
        views.booking_confirmation,
        name="booking_confirmation",
    ),
    path("my-bookings/", views.my_bookings, name="my_bookings"),
    path("about/", views.about, name="about"),
    # Authentication URLs
    path("register/", views.register, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="booking/login.html"),
        name="login",
    ),
    path("logout/", views.custom_logout, name="logout"),
    # Password reset URLs
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="booking/password_reset.html"
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="booking/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="booking/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="booking/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
