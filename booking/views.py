from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate, logout
from django.utils import timezone
from django.db.models import Q
from django.http import JsonResponse
from datetime import datetime, date, timedelta  # Add these imports

import logging

from .models import FitnessClass, Booking, UserProfile
from .forms import UserRegisterForm, BookingForm, UserProfileForm

# Set up logging
logger = logging.getLogger(__name__)

def home(request):
    # Get upcoming classes for the home page
    upcoming_classes = FitnessClass.objects.filter(
        date__gte=timezone.now().date()
    ).order_by('date', 'start_time')[:3]
    
    return render(request, 'booking/index.html', {'classes': upcoming_classes})

def about(request):
    """View function for the about us page."""
    return render(request, 'booking/about.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            
            # Try to send email, but don't fail if it doesn't work
            try:
                # Get current site domain for absolute URLs
                current_site = request.META['HTTP_HOST']
                site_url = f"{'https://' if request.is_secure() else 'http://'}{current_site}"
                
                # Render the HTML email
                html_message = render_to_string('booking/emails/welcome_email.html', {
                    'user': user,
                    'site_url': site_url
                })
                
                # Plain text fallback
                plain_message = f"Hi {user.first_name},\n\nThank you for registering with our Fitness Class Booking System!"
                
                send_mail(
                    'Welcome to FitBook!',
                    plain_message,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    html_message=html_message,
                    fail_silently=True,
                )
            except Exception as e:
                logger.warning(f"Failed to send welcome email: {str(e)}")
            
            return redirect('login')
    else:
        form = UserRegisterForm()
    
    return render(request, 'booking/register.html', {'form': form})

@login_required
def classes(request):
    # Initialize filter variables
    query = request.GET.get('query', '')
    category = request.GET.get('category', '')
    
    # Get all classes (not just upcoming ones) to show everything in the database
    all_classes = FitnessClass.objects.all().order_by('date', 'start_time')
    
    # Apply filters if provided
    if query:
        all_classes = all_classes.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(instructor__icontains=query)
        )
    
    if category:
        all_classes = all_classes.filter(category=category)
    
    # Get user's bookings to check which classes are already booked
    user_bookings = Booking.objects.filter(user=request.user).values_list('fitness_class_id', flat=True)
    
    # Add booking status to each class
    for fitness_class in all_classes:
        fitness_class.is_booked = fitness_class.id in user_bookings
        fitness_class.is_available = not fitness_class.is_full
    
    # Get all categories for the filter dropdown
    try:
        categories = FitnessClass.CATEGORY_CHOICES
    except AttributeError:
        # Fallback if CATEGORY_CHOICES is not defined in the model
        categories = []
    
    # Separate featured classes (first 2) and initial display classes (next 6)
    featured_classes = all_classes[:2]
    initial_classes = all_classes[2:8]
    remaining_classes = all_classes[8:]
    
    context = {
        'featured_classes': featured_classes,
        'initial_classes': initial_classes,
        'remaining_classes': remaining_classes,
        'all_classes': all_classes,
        'categories': categories,
        'selected_category': category,
        'query': query,
        'has_more_classes': len(remaining_classes) > 0
    }
    
    return render(request, 'booking/classes.html', context)

# AJAX endpoint to load more classes
@login_required
def load_more_classes(request):
    offset = int(request.GET.get('offset', 8))  # Default to skip the first 8 classes (2 featured + 6 initial)
    limit = int(request.GET.get('limit', 6))    # Load 6 more by default
    
    # Get the next batch of classes
    classes = FitnessClass.objects.all().order_by('date', 'start_time')[offset:offset+limit]
    
    # Get user's bookings to check which classes are already booked
    user_bookings = Booking.objects.filter(user=request.user).values_list('fitness_class_id', flat=True)
    
    # Build the HTML for the additional classes
    class_html = []
    for i, fitness_class in enumerate(classes):
        fitness_class.is_booked = fitness_class.id in user_bookings
        fitness_class.is_available = not fitness_class.is_full
        
        # You'd render each class card here, but this is simplified
        # In a real implementation, you might use a template fragment
        class_html.append({
            'id': fitness_class.id,
            'name': fitness_class.name,
            'description': fitness_class.description,
            'date': str(fitness_class.date),
            'start_time': str(fitness_class.start_time),
            'end_time': str(fitness_class.end_time),
            'instructor': fitness_class.instructor,
            'is_full': fitness_class.is_full,
            'is_booked': fitness_class.is_booked
        })
    
    # Check if there are more classes to load
    has_more = FitnessClass.objects.all().count() > offset + limit
    
    return JsonResponse({
        'classes': class_html,
        'has_more': has_more,
        'next_offset': offset + limit
    })

@login_required
def book_class(request, class_id):
    fitness_class = get_object_or_404(FitnessClass, id=class_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        
        if form.is_valid():
            # Check if user already booked this class
            if Booking.objects.filter(user=request.user, fitness_class=fitness_class).exists():
                messages.warning(request, f'You have already booked {fitness_class.name}!')
                return redirect('classes')
                
            # Check if class is full
            if fitness_class.is_full:
                messages.warning(request, f'Sorry, {fitness_class.name} is already full!')
                return redirect('classes')
                
            # Create booking
            booking = form.save(commit=False)
            booking.user = request.user
            booking.fitness_class = fitness_class
            booking.save()
            
            # Try to send confirmation email, but don't fail if it doesn't work
            try:
                # Get current site domain for absolute URLs
                current_site = request.META['HTTP_HOST']
                site_url = f"{'https://' if request.is_secure() else 'http://'}{current_site}"
                
                # Render the HTML email
                html_message = render_to_string('booking/emails/booking_confirmation.html', {
                    'user': request.user,
                    'booking': booking,
                    'site_url': site_url
                })
                
                # Plain text fallback
                plain_message = f"Hi {request.user.first_name},\n\nYour booking for {fitness_class.name} on {fitness_class.date} at {fitness_class.start_time} has been confirmed!"
                
                send_mail(
                    f'Your FitBook Booking Confirmation: {fitness_class.name}',
                    plain_message,
                    settings.EMAIL_HOST_USER,
                    [request.user.email],
                    html_message=html_message,
                    fail_silently=True,
                )
            except Exception as e:
                logger.warning(f"Failed to send booking confirmation email: {str(e)}")
            
            messages.success(request, f'You have successfully booked {fitness_class.name}!')
            return redirect('booking_confirmation', booking_id=booking.id)
    else:
        form = BookingForm()
        
    return render(request, 'booking/book_class.html', {'form': form, 'fitness_class': fitness_class})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if request.method == 'POST':
        class_name = booking.fitness_class.name
        
        # Store booking info before deletion for email
        fitness_class = booking.fitness_class
        
        booking.delete()
        
        # Try to send cancellation email, but don't fail if it doesn't work
        try:
            # Get current site domain for absolute URLs
            current_site = request.META['HTTP_HOST']
            site_url = f"{'https://' if request.is_secure() else 'http://'}{current_site}"
            
            # Render the HTML email
            html_message = render_to_string('booking/emails/booking_cancellation.html', {
                'user': request.user,
                'booking': {
                    'fitness_class': fitness_class
                },
                'site_url': site_url
            })
            
            # Plain text fallback
            plain_message = f"Hi {request.user.first_name},\n\nYour booking for {class_name} has been cancelled."
            
            send_mail(
                'Your FitBook Booking Cancellation',
                plain_message,
                settings.EMAIL_HOST_USER,
                [request.user.email],
                html_message=html_message,
                fail_silently=True,
            )
        except Exception as e:
            logger.warning(f"Failed to send booking cancellation email: {str(e)}")
        
        messages.success(request, f'Your booking for {class_name} has been cancelled.')
        return redirect('classes')
        
    return render(request, 'booking/cancel_booking.html', {'booking': booking})

@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'booking/booking_confirmation.html', {'booking': booking})

@login_required
def my_bookings(request):
    # Get all bookings for the current user and order them by class date and time
    bookings = Booking.objects.filter(user=request.user).order_by('fitness_class__date', 'fitness_class__start_time')
    
    # Debug: Log the number of bookings found
    print(f"Found {bookings.count()} bookings for user {request.user.username}")
    
    # Calculate statistics for the dashboard
    today = timezone.now().date()
    
    # Get upcoming bookings
    upcoming_bookings = [b for b in bookings if b.fitness_class.date >= today]
    upcoming_count = len(upcoming_bookings)
    
    # Calculate total hours
    total_hours = 0
    for booking in bookings:
        if hasattr(booking.fitness_class, 'start_time') and hasattr(booking.fitness_class, 'end_time'):
            start_time = booking.fitness_class.start_time
            end_time = booking.fitness_class.end_time
            if start_time and end_time:
                # Calculate duration in hours
                duration = (datetime.combine(date.min, end_time) - datetime.combine(date.min, start_time)).seconds / 3600
                total_hours += duration
    
    # Find favorite class type
    class_types = {}
    for booking in bookings:
        class_type = booking.fitness_class.category if hasattr(booking.fitness_class, 'category') else 'Unknown'
        if class_type in class_types:
            class_types[class_type] += 1
        else:
            class_types[class_type] = 1
    
    favorite_class = "None"
    if class_types:
        favorite_class = max(class_types, key=class_types.get)
    
    # Prepare context data
    context = {
        'bookings': bookings,
        'upcomingClasses': upcoming_count,
        'totalHours': round(total_hours),
        'favoriteClass': favorite_class,
        'today': today,
        # Ensure we always pass these values to avoid template errors
        'has_bookings': bookings.exists(),
    }
    
    return render(request, 'booking/my_bookings.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        user_form = UserRegisterForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    
    return render(request, 'booking/profile.html', context)

def custom_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')