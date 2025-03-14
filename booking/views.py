from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import FitnessClass, Booking
from .forms import UserRegisterForm, BookingForm, UserProfileForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.shortcuts import redirect

def home(request):
    classes = FitnessClass.objects.all().order_by('date', 'start_time')
    return render(request, 'booking/index.html', {'classes': classes})

def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            
            username = user_form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            
            # Send welcome email
            send_mail(
                'Welcome to Fitness Booking System',
                f'Hi {username},\n\nThank you for registering with our Fitness Class Booking System!',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            
            return redirect('login')
    else:
        user_form = UserRegisterForm()
        profile_form = UserProfileForm()
        
    return render(request, 'booking/register.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def classes(request):
    classes = FitnessClass.objects.all().order_by('date', 'start_time')
    user_bookings = Booking.objects.filter(user=request.user).values_list('fitness_class_id', flat=True)
    
    for fitness_class in classes:
        fitness_class.is_booked = fitness_class.id in user_bookings
        fitness_class.is_available = not fitness_class.is_full
        
    return render(request, 'booking/classes.html', {'classes': classes})

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
            
            # Send confirmation email
            send_mail(
                'Booking Confirmation',
                f'Hi {request.user.username},\n\nYour booking for {fitness_class.name} on {fitness_class.date} at {fitness_class.start_time} has been confirmed!',
                settings.EMAIL_HOST_USER,
                [request.user.email],
                fail_silently=False,
            )
            
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
        booking.delete()
        
        # Send cancellation email
        send_mail(
            'Booking Cancellation',
            f'Hi {request.user.username},\n\nYour booking for {class_name} has been cancelled.',
            settings.EMAIL_HOST_USER,
            [request.user.email],
            fail_silently=False,
        )
        
        messages.success(request, f'Your booking for {class_name} has been cancelled.')
        return redirect('classes')
        
    return render(request, 'booking/cancel_booking.html', {'booking': booking})

@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'booking/booking_confirmation.html', {'booking': booking})

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('fitness_class__date', 'fitness_class__start_time')
    return render(request, 'booking/my_bookings.html', {'bookings': bookings})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'booking/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'booking/login.html')

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('fitness_class__date', 'fitness_class__start_time')
    return render(request, 'booking/my_bookings.html', {'bookings': bookings})
def custom_logout(request):
    logout(request)
    return redirect('home')