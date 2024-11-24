from django.shortcuts import render, redirect, get_object_or_404
from .models import Team, ContactMessage
from cars.models import Car
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from .forms import CarForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login



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
    if request.user.is_authenticated:
        # Get all cars listed by the current logged-in user
        cars = Car.objects.filter(seller=request.user)
        return render(request, 'pages/sell.html', {'cars': cars, 'is_logged_in': True})
    else:
        # No cars to show for non-logged-in users
        return render(request, 'pages/sell.html', {'is_logged_in': False})


@login_required
def add_car(request):
    # Handling the form for adding a new car
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



@login_required
def edit_car(request, car_id):
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



@login_required
def delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id, seller=request.user)  # Ensure the car belongs to the logged-in user
    car.delete()
    messages.success(request, 'Car deleted successfully!')
    return redirect('sell')  # Redirect back to the sell page after deleting the car



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