from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date, time
from .models import FitnessClass, Booking, UserProfile

class FitnessClassModelTest(TestCase):
    def setUp(self):
        self.fitness_class = FitnessClass.objects.create(
            name="Yoga",
            description="Relaxing yoga class",
            instructor="John Doe",
            date=date(2025, 3, 15),
            start_time=time(10, 0),
            end_time=time(11, 0),
            capacity=10
        )

    def test_string_representation(self):
        self.assertEqual(str(self.fitness_class), "Yoga - 2025-03-15 10:00:00")

    def test_is_full_property(self):
        # Class should not be full initially
        self.assertFalse(self.fitness_class.is_full)
        
        # Create users and bookings to fill the class
        for i in range(10):
            user = User.objects.create_user(
                username=f"testuser{i}",
                email=f"testuser{i}@example.com",
                password="testpassword"
            )
            Booking.objects.create(
                user=user,
                fitness_class=self.fitness_class
            )
        
        # Class should now be full
        self.assertTrue(self.fitness_class.is_full)

class BookingViewsTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="testpassword"
        )
        UserProfile.objects.create(
            user=self.user,
            phone="1234567890"
        )
        
        # Create a fitness class
        self.fitness_class = FitnessClass.objects.create(
            name="Pilates",
            description="Core strength training",
            instructor="Jane Smith",
            date=date(2025, 3, 20),
            start_time=time(14, 0),
            end_time=time(15, 0),
            capacity=5
        )
    
    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/index.html')
        self.assertContains(response, 'Pilates')
    
    def test_classes_view_requires_login(self):
        # Should redirect if not logged in
        response = self.client.get(reverse('classes'))
        self.assertEqual(response.status_code, 302)
        
        # Log in and try again
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('classes'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking/classes.html')
    
    def test_book_class(self):
        self.client.login(username='testuser', password='testpassword')
        
        # Initially, no bookings should exist
        self.assertEqual(Booking.objects.count(), 0)
        
        # Book a class
        response = self.client.post(reverse('book_class', args=[self.fitness_class.id]))
        
        # Should have created a booking
        self.assertEqual(Booking.objects.count(), 1)
        booking = Booking.objects.first()
        self.assertEqual(booking.user, self.user)
        self.assertEqual(booking.fitness_class, self.fitness_class)
        
        # Should redirect to confirmation page
        self.assertRedirects(response, reverse('booking_confirmation', args=[booking.id]))