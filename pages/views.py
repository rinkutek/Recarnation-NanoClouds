from django.shortcuts import render, redirect, get_object_or_404
from .models import Team, ContactMessage
from cars.models import Car
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from .forms import CarForm 
import pandas as pd
import numpy as np
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from contacts.models import Contact

# Precompute weight coefficients for prediction
# `w_0` is the intercept and `w` contains the weights for the model
# w_0 , w = w_calc()

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


from django.shortcuts import render
import pandas as pd
import numpy as np
from .car_used import model  # make sure car.py defines and exports the model

def predict(request):
    """
    Handles car price prediction from user input using the used_cars.csv-trained XGBoost model.
    """
    if request.method == 'POST':
        try:
            # Collect form data
            car_data = {
                'brand': request.POST['brand'],
                'model': request.POST['model'],
                'fuel_type': request.POST['fuel_type'],
                'engine': request.POST['engine'],
                'transmission': request.POST['transmission'],
                'ext_col': request.POST['ext_col'],
                'int_col': request.POST['int_col'],
                'accident': request.POST['accident'],
                'clean_title': request.POST['clean_title'],
                'milage': int(request.POST['milage']),
                'age': 2024 - int(request.POST['model_year'])  # Derived from model_year
            }

            # Convert to DataFrame
            input_df = pd.DataFrame([car_data])

            # Predict using model
            log_price_pred = model.predict(input_df)[0]
            predicted_price = int(np.expm1(log_price_pred)* 0.70)  # Convert from log price
            context = {
                'price': predicted_price
            }
            return render(request, 'pages/carprice.html', context)

        except Exception as e:
            return render(request, 'pages/carprice.html', {'error': str(e)})

    return render(request, 'pages/carprice.html')
