from django.shortcuts import render, redirect, get_object_or_404
from .models import Team, ContactMessage
from cars.models import Car
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from .forms import CarForm
from .car import w_calc,prepare_X
import pandas as pd
import numpy as np
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from contacts.models import Contact

# Precompute weight coefficients for prediction
# `w_0` is the intercept and `w` contains the weights for the model
w_0 , w = w_calc()

# Function to display the homepage
def home(request):
    """
    Displays the homepage.
    - Fetches all teams and featured cars from the database.
    - Provides search options for models, cities, years, and body styles.
    - Renders the 'home.html' template with the fetched data.
    """
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

# Function to display the About page
def about(request):
    """
    Displays the About Us page.
    - Fetches team data from the database to showcase team members.
    - Renders the 'about.html' template with team data.
    """
    teams = Team.objects.all()
    data = {
        'teams': teams,
    }
    return render(request, 'pages/about.html', data)

# Function to display the Sell page
def sell(request):
    """
    Displays the Sell page for authenticated users.
    - Fetches cars listed by the logged-in user.
    - Attaches related inquiries to each car.
    - Redirects non-authenticated users to the login page with an error message.
    """
    if request.user.is_authenticated:
        # Fetch all cars listed by the logged-in seller
        cars = Car.objects.filter(seller=request.user)

        # Attach inquiries to each car
        for car in cars:
            car.inquiries = Contact.objects.filter(car_id=car.id)

        return render(request, 'pages/sell.html', {
            'cars': cars,
            'is_logged_in': True
        })
    else:
        # Redirect non-authenticated users to login
        messages.error(request, "You need to log in to view your listings.")
        return redirect('login')

# Function to add a car
@login_required
def add_car(request):
    """
    Handles adding a new car.
    - Displays a form to input car details.
    - Saves the new car with 'Pending' status and assigns the logged-in user as the seller.
    - Redirects to the Sell page on success or shows the form with validation errors.
    """
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.seller = request.user  # Assign the logged-in user as the seller
            car.status = 'Pending'  # Default status
            car.save()
            messages.success(request, 'Car added successfully!')
            return redirect('sell')  # Redirect back to the sell page to show the newly added car
    else:
        form = CarForm()

    return render(request, 'pages/add_car.html', {'form': form})


# Function to edit a car
@login_required
def edit_car(request, car_id):
    """
    Handles editing an existing car.
    - Ensures the car belongs to the logged-in user.
    - Displays a form pre-filled with car details.
    - Saves changes and redirects to the Sell page on success.
    """
    try:
        car = Car.objects.get(id=car_id, seller=request.user)  # Ensure the car belongs to the logged-in user
    except Car.DoesNotExist:
        car = None  # No car found for the user

    if car is None:
        messages.error(request, "No car found to edit. Please add a car first.")
        return redirect('sell')  # Redirect back to the sell page if the car is not found

    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            messages.success(request, 'Car details updated successfully!')
            return redirect('sell')  # Redirect back to the sell page after saving changes
    else:
        form = CarForm(instance=car)

    return render(request, 'pages/edit_car.html', {'form': form, 'car': car})


# Function to delete a car
@login_required
def delete_car(request, car_id):
    """
    Handles deleting a car.
    - Ensures the car belongs to the logged-in user.
    - Deletes the car and redirects to the Sell page with a success message.
    """
    car = get_object_or_404(Car, id=car_id, seller=request.user)  # Ensure the car belongs to the logged-in user
    car.delete()
    messages.success(request, 'Car deleted successfully!')
    return redirect('sell')  # Redirect back to the sell page after deleting the car



# Function to handle the contact form
def contact(request):
    """
    Handles the contact form submission.
    - Collects form data from the POST request and saves it in the database.
    - Displays a success message and redirects back to the Contact page.
    """
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

# Function to predict car prices
def predict(request):
    """
    Handles car price prediction.
    - Accepts car attributes from a POST request.
    - Prepares input data and applies the prediction model to estimate the price.
    - Renders the prediction result on the same page.
    """
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
