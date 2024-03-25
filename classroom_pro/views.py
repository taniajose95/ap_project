from django.shortcuts import render, redirect
from .models import Room, Booking, User
from django.contrib import messages
from django.contrib.auth import authenticate, login

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

def login_view(request):
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