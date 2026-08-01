from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, SeminarHallForm, BookingForm
from .models import SeminarHall, Booking
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Booking
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


def home(request):
    return render(request, 'accounts/home.html')


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('home')

    return render(request, 'accounts/login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def add_hall(request):
    if request.method == "POST":
        form = SeminarHallForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            print(form.errors)   # Temporary debugging

    else:
        form = SeminarHallForm()

    return render(request, 'accounts/hall_form.html', {'form': form})

@login_required
def hall_list(request):

    halls = SeminarHall.objects.all()

    search = request.GET.get('search')
    location = request.GET.get('location')
    capacity = request.GET.get('capacity')

    if search:
        halls = halls.filter(hall_name__icontains=search)

    if location:
        halls = halls.filter(location__icontains=location)

    if capacity:
        halls = halls.filter(capacity__gte=capacity)

    context = {
        'halls': halls,
        'search': search,
        'location': location,
        'capacity': capacity,
    }

    return render(request, 'accounts/hall_list.html', context)
    
@login_required
def edit_hall(request, id):
    hall = get_object_or_404(SeminarHall, id=id)

    if request.method == "POST":
        form = SeminarHallForm(
    request.POST,
    request.FILES,
    instance=hall
)

        if form.is_valid():
            form.save()
            return redirect('hall_list')
    else:
        form = SeminarHallForm(instance=hall)

    return render(request, 'accounts/hall_form.html', {'form': form})

@login_required  
def delete_hall(request, id):
    hall = get_object_or_404(SeminarHall, id=id)

    hall.delete()

    return redirect('hall_list')

@login_required
def book_hall(request):

    if request.method == "POST":

        form = BookingForm(request.POST)

        if form.is_valid():

            hall = form.cleaned_data['hall']
            booking_date = form.cleaned_data['booking_date']
            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']

            # Check for overlapping bookings
            existing_booking = Booking.objects.filter(
                hall=hall,
                booking_date=booking_date,
                start_time__lt=end_time,
                end_time__gt=start_time
            ).exists()

            if existing_booking:

                form.add_error(
                    None,
                    "This hall is already booked during the selected time."
                )

            else:

                booking = form.save(commit=False)
                booking.user = request.user
                booking.save()

                return redirect('my_bookings')

    else:

        form = BookingForm()

    return render(
        request,
        'accounts/book_hall.html',
        {'form': form}
    )

@login_required
def my_bookings(request):

    bookings = Booking.objects.filter(user=request.user)

    return render(
        request,
        'accounts/my_bookings.html',
        {'bookings': bookings}
    )

@login_required
def dashboard(request):
    total_bookings = Booking.objects.filter(user=request.user).count()
    pending = Booking.objects.filter(user=request.user, status='Pending').count()
    approved = Booking.objects.filter(user=request.user, status='Approved').count()
    rejected = Booking.objects.filter(user=request.user, status='Rejected').count()

    context = {
        'total_bookings': total_bookings,
        'pending': pending,
        'approved': approved,
        'rejected': rejected,
    }

    return render(request, 'accounts/dashboard.html', context)

@login_required
def admin_dashboard(request):

    total_users = User.objects.count()
    total_halls = SeminarHall.objects.count()
    total_bookings = Booking.objects.count()

    pending = Booking.objects.filter(status='Pending').count()
    approved = Booking.objects.filter(status='Approved').count()
    rejected = Booking.objects.filter(status='Rejected').count()

    context = {
        'total_users': total_users,
        'total_halls': total_halls,
        'total_bookings': total_bookings,
        'pending': pending,
        'approved': approved,
        'rejected': rejected,
    }

    return render(request, 'accounts/admin_dashboard.html', context)