from django.shortcuts import render, redirect
from .models import Room, Booking, User
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.conf import settings



def index(request):
    # You can add any context data needed for rendering the template
    context = {
        'welcome_message': 'Welcome to our Classroom Pro application!',
    }
    return render(request, 'index.html', context)

def room_list(request):
    rooms = Room.objects.all()
    print(rooms)
    return render(request, 'room_list.html', {'rooms': rooms})

def book_room(request, room_id):
    if request.method == 'POST':
        user_id = request.POST['user_id']  # Assuming user ID is submitted via form
        date = request.POST['date']
        time_slot = request.POST['time_slot']
        room = Room.objects.get(pk=room_id)
        user = User.objects.get(pk=user_id)
        # Check if the room is available for booking
        if Booking.objects.filter(Room=room, Date=date, TimeSlot=time_slot).exists():
            messages.error(request, 'The room is already booked for this time slot.')
            return redirect('room_list')
        else:
            booking = Booking.objects.create(Room=room, User=user, Date=date, TimeSlot=time_slot)
            messages.success(request, 'Room booked successfully.')
            return redirect('room_list')
    else:
        room = Room.objects.get(pk=room_id)
        return render(request, 'book_room.html', {'room': room})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            role = form.cleaned_data.get('role')
            department = form.cleaned_data.get('department')
            password = form.cleaned_data.get('password1')

            user = User.objects.create(
                UserID='',
                Name=name,
                Email=email,
                Role=role,
                Department=department,
                user_password=password
            )
            user.save()
            return redirect('login')  # Redirect to login page after signup
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def manage_booking(request):
    # Fetch bookings from the database
    bookings = Booking.objects.all()
    return render(request, 'manage_booking.html', {'bookings': bookings})


def login(request):
    if request.method == 'POST':
        action = request.POST.get('action')  # Check if it's a login or sign-up request
        if action == 'login':
            # Handle login logic
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redirect to a specific URL after login (e.g., room list page)
                return redirect('room_list')
            else:
                # Invalid login credentials
                return render(request, 'login.html', {'error_message': 'Invalid username or password'})
        elif action == 'signup':
            # Handle sign-up logic
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            # Check if the username is already taken
            if User.objects.filter(username=username).exists():
                return render(request, 'login.html', {'error_message': 'Username is already taken'})
            else:
                # Create a new user and save it to the database
                user = User.objects.create_user(username=username, email=email, password=password)
                login(request, user)
                # Redirect to a specific URL after sign-up (e.g., room list page)
                return redirect('room_list')
    else:
        return render(request, 'login.html')

def cancel_booking(request, booking_id):
    booking = Booking.objects.get(BookingID=booking_id)
    # Delete the booking
    booking.delete()
    return redirect('manage_booking')

def modify_booking(request, booking_id):
    booking = Booking.objects.get(BookingID=booking_id)
    if request.method == 'POST':
        new_time_slot = request.POST.get('time_slot')
        # Update time slot in Booking table
        booking.TimeSlot = new_time_slot
        booking.save()
        # Update availability status in RoomAvailability table (assuming you want to mark the old slot as available)
        old_time_slot_availability = RoomAvailability.objects.get(RoomID=booking.RoomID, Date=booking.Date, TimeSlot=booking.TimeSlot)
        old_time_slot_availability.AvailabilityStatus = 'available'
        old_time_slot_availability.save()
        new_time_slot_availability = RoomAvailability.objects.get(RoomID=booking.RoomID, Date=booking.Date, TimeSlot=new_time_slot)
        new_time_slot_availability.AvailabilityStatus = 'booked'
        new_time_slot_availability.save()
        return redirect('manage_booking')
    else:
        room_availabilities = RoomAvailability.objects.filter(RoomID=booking.RoomID, AvailabilityStatus='available')
        return render(request, 'modify_booking.html', {'room_availabilities': room_availabilities})