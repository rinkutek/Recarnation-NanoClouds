from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver

# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')

# def register(request):
#     if request.method == 'POST':
#         firstname = request.POST['firstname']
#         lastname = request.POST['lastname']
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']
#         confirm_password = request.POST['confirm_password']

#         if password == confirm_password:
#             if User.objects.filter(username=username).exists():
#                 messages.error(request, 'Username already exists!')
#                 return redirect('register')
#             else:
#                 if User.objects.filter(email=email).exists():
#                     messages.error(request, 'Email already exists!')
#                     return redirect('register')
#                 else:
#                     user = User.objects.create_user(first_name=firstname, last_name=lastname, email=email, username=username, password=password)
#                     auth.login(request, user)
#                     messages.success(request, 'You are now logged in.')
#                     return redirect('dashboard')
#                     user.save()
#                     messages.success(request, 'You are registered successfully.')
#                     return redirect('login')
#         else:
#             messages.error(request, 'Password do not match')
#             return redirect('register')
#     else:
#         return render(request, 'accounts/register.html')

def register(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        # Check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('register')

        # Check if email exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return redirect('register')

        # Create and save the user
        user = User.objects.create_user(
            first_name=firstname,
            last_name=lastname,
            email=email,
            username=username,
            password=password
        )
        user.save()  # Ensure the user is saved to the database

        # Log the user in using the basic authentication backend
        auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request, 'Registration successful! You are now logged in.')
        return redirect('dashboard')

    return render(request, 'accounts/register.html')

    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        # Check if username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('register')

        # Check if email exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return redirect('register')

        # Create and save the user
        user = User.objects.create_user(
            first_name=firstname,
            last_name=lastname,
            email=email,
            username=username,
            password=password
        )
        user.save()  # Ensure user is saved to the database

        # Log the user in after registration
        auth.login(request, user)
        messages.success(request, 'Registration successful! You are now logged in.')
        return redirect('dashboard')

    else:
        return render(request, 'accounts/register.html')



@login_required(login_url = 'login')
def dashboard(request):
    user_inquiry = Contact.objects.order_by('-create_date').filter(user_id=request.user.id)
    data = {
        'inquiries': user_inquiry,
    }
    return render(request, 'accounts/dashboard.html', data)

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
    return redirect('home')
