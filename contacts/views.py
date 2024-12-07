from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from cars.models import Car  # Import Car model
from .models import Contact
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Function for car inquiry
@login_required
def inquiry(request):
    if request.method == 'POST':
        car_id = request.POST['car_id']
        car_title = request.POST['car_title']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        customer_need = request.POST['customer_need']
        city = request.POST['city']
        state = request.POST['state']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.user.id #if request.user.is_authenticated else None

        try:
            # Validate car existence
            car = Car.objects.get(id=car_id)
            # Save the inquiry
            contact = Contact(
                car_id=car_id,
                car_title=car_title,
                first_name=first_name,
                last_name=last_name,
                customer_need=customer_need,
                city=city,
                state=state,
                email=email,
                phone=phone,
                message=message,
                user_id=user_id,
                create_date=timezone.now(),  # Use timezone-aware datetime
            )
            contact.save()

            # Email to the seller
            seller_email = car.seller_email
            seller_phone = car.seller_phone
            if seller_email:
                seller_subject = f"Inquiry for {car_title}"
                seller_message = (
                    f"Dear Seller,\n\n"
                    f"You have received a new inquiry for your car listing '{car_title}'.\n\n"
                    f"Customer Details:\n"
                    f"Name: {first_name} {last_name}\n"
                    f"Email: {email}\n"
                    f"Phone: {phone}\n"
                    f"Location: {city}, {state}\n"
                    f"Need: {customer_need}\n\n"
                    f"Message:\n{message}\n\n"
                    f"Best Regards,\nCar Dealer Platform"
                )
                send_mail(
                    seller_subject,
                    seller_message,
                    'recarnationtechtitans@gmail.com',
                    [seller_email],
                    fail_silently=False                )

            messages.success(request, "Your inquiry has been submitted successfully!")
            return redirect(f'/cars/{car_id}')
        
        except Car.DoesNotExist:
            messages.error(request, "The car you are inquiring about does not exist.")
            return redirect('home')

    else:
        return redirect('home')
