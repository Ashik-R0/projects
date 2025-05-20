from django.shortcuts import render,redirect
from .models import Tourpakage
from django.utils.timezone import now
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Booking
from django.contrib.auth.decorators import login_required
from .forms import TourPackageForm 

from django.conf import settings
from datetime import datetime

# Create your views here.
from django.db.models import Q

def home(request):

    clean_expired_packages()
   
    trending_packages = Tourpakage.objects.filter(
        trending=True,
        is_active=True,
        is_approved=True,
        price__lt=20000  
    )

    search_query = request.GET.get('query')
    search_results = []

    if search_query:
        search_results = Tourpakage.objects.filter(
            is_active=True
        ).filter(
            Q(title__icontains=search_query) | Q(location__icontains=search_query)
        )

    return render(request, 'home.html', {
        'packages': trending_packages,
        'search_results': search_results,
        'search_query': search_query,
    })


@login_required
def vendorpage(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        messages.error(request, "No user profile found. Please contact admin or register again.")
        return redirect('home')

    if profile.role != 'vendor':
        return redirect('home') 

    if request.method == 'POST':
        title = request.POST.get('title')
        price = request.POST.get('price')
        duration = request.POST.get('duration')
        image = request.FILES.get('image')
        description = request.POST.get('description')
        location = request.POST.get('location')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        trending = True

        
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid date format.")
            return redirect('vendorpage')

        Tourpakage.objects.create(
            title=title,
            price=price,
            duration=duration,
            image=image,
            description=description,
            trending=trending,
            location=location,
            start_date=start_date,
            end_date=end_date,
            vendor=request.user
        )

        messages.success(request, "Tour package uploaded successfully.")
        return redirect('home')

    return render(request, 'vendorpage.html')


def auth_view(request):
    if request.method == "POST":
        if 'username' in request.POST: 
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            role = request.POST['role']
            if User.objects.filter(username=email).exists():
                messages.error(request, "Email already registered.")
            else:
                user = User.objects.create_user(username=email, email=email, password=password, first_name=username)

                UserProfile.objects.create(user=user, role=role)
                login(request, user)
                return redirect('home')
        else:  
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, "Invalid usename or password.")
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

from django.shortcuts import get_object_or_404

@login_required
def explore(request, package_id):
    package = get_object_or_404(Tourpakage, id=package_id)
    return render(request, 'explore.html', {'package': package})

def details(request):
    clean_expired_packages()
    packages = Tourpakage.objects.filter(is_active=True,is_approved=True)
    return render(request, 'details.html', {'packages': packages})

def clean_expired_packages():
    Tourpakage.objects.filter(end_date__lt=now().date()).delete()



@login_required
def book_tour(request, package_id):
    tour = get_object_or_404(Tourpakage, id=package_id)
    
    if request.method == 'POST':
        number_of_people = int(request.POST.get('number_of_people', 1))
        
        Booking.objects.create(user=request.user, tour=tour, number_of_people=number_of_people)
        return redirect('booked_tours')

    return render(request, 'book_tour.html', {'tour': tour}) 


@login_required
def booked_tours(request):
    bookings = Booking.objects.filter(user=request.user).select_related('tour').order_by('-booking_date')
    return render(request, 'booked_tours.html', {'bookings': bookings})

@login_required
def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.delete()
    return redirect('booked_tours')
@login_required
def my_packages(request):
    if request.user.userprofile.role != 'vendor':
        return redirect('home')  

    packages = Tourpakage.objects.filter(vendor=request.user)
    return render(request, 'my_packages.html', {'packages': packages})

@login_required
def edit_package(request, pk):
    package = get_object_or_404(Tourpakage, id=pk, vendor=request.user)

    if request.method == 'POST':
        form = TourPackageForm(request.POST, request.FILES, instance=package)
        if form.is_valid():
            form.save()
            return redirect('my_packages')
    else:
        form = TourPackageForm(instance=package)

    return render(request, 'edit_package.html', {'form': form})
@login_required
def delete_package(request, pk):
    package = get_object_or_404(Tourpakage, id=pk, vendor=request.user)
    package.delete()
    return redirect('my_packages')

def clean_expired_packages():
    Tourpakage.objects.filter(end_date__lt=now().date()).update(is_active=False)
