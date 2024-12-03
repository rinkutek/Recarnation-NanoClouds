from django.shortcuts import render, redirect
from .models import Team, ContactMessage
from cars.models import Car
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from .forms import CarForm
from .car import w_calc,prepare_X
import pandas as pd
import numpy as np

w_0 , w = w_calc()

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

def predict(request):
    
    if request.method =='POST':
     
        df ={
            'make': request.POST['make'],
            'model': request.POST['model'],
            'year': int(request.POST['year']),
            'engine_fuel_type': request.POST['engine_fuel_type'],
            'engine_hp': int(request.POST['engine_hp']),
            'engine_cylinders': int(request.POST['engine_cylinders']),
            'transmission_type': request.POST['transmission_type'],
            'driven_wheels': request.POST['driven_wheels'],
            'number_of_doors': int(request.POST['number_of_doors']),
            'market_category': request.POST['market_category'],
            'vehicle_size': request.POST['vehicle_size'],
            'vehicle_style': request.POST['vehicle_style'],
            'highway_mpg': int(request.POST['highway_mpg']),
            'city_mpg': int(request.POST['city_mpg']),
            'popularity':int(request.POST['popularity']) ,
            
        }
        
        X_test = prepare_X(pd.DataFrame([df]))
        y_pred = w_0 + X_test.dot(w)
        price  = np.expm1(y_pred)[0].astype(int)
        print(price)
        
        context = {
            'price':price ,
        }
        
        return render(request , 'pages/carprice.html',context)

    else:
        
        return render(request , 'pages/carprice.html')
