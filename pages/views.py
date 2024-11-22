from django.shortcuts import render, redirect
from .models import Team, ContactMessage
from cars.models import Car
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from .forms import CarForm


# Create your views here.

def home(request):
    teams = Team.objects.all()
    featured_cars = Car.objects.order_by('-created_date').filter(is_featured=True)
    all_cars = Car.objects.order_by('-created_date')
    model_search = Car.objects.values_list('model', flat=True).distinct()
    city_search = Car.objects.values_list('city', flat=True).distinct()
    year_search = Car.objects.values_list('year', flat=True).distinct()
    body_style_search = Car.objects.values_list('body_style', flat=True).distinct()
    data = {
        'teams': teams,
        'featured_cars': featured_cars,
        'all_cars': all_cars,
        'model_search': model_search,
        'city_search': city_search,
        'year_search': year_search,
        'body_style_search': body_style_search,
    }
    return render(request, 'pages/home.html', data)


def about(request):
    teams = Team.objects.all()
    data = {
        'teams': teams,
    }
    return render(request, 'pages/about.html', data)

def sell(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.seller = request.user  # Set the logged-in user as the seller
            car.status = 'Pending'  # Default status
            car.save()
            return redirect('dashboard')  # Redirect to seller dashboard
    else:
        form = CarForm()

    return render(request, 'pages/sell.html', {'form': form})

def contact(request):
    if request.method == 'POST':
        # Getting form data from POST request
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        phone = request.POST['phone']
        message = request.POST['message']

        # Create a new ContactMessage instance
        contact_message = ContactMessage(
            name=name,
            email=email,
            subject=subject,
            phone=phone,
            message=message
        )
        # Save the contact message to the database
        contact_message.save()

        # Display success message to the user
        messages.success(request, 'Thank you for contacting us. We will get back to you shortly')
        return redirect('contact')

    return render(request, 'pages/contact.html')