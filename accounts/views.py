from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver

# Function for user login
def login(request):
    """
    Handles user login functionality.
    - Accepts username and password from the POST request.
    - Authenticates the user using Django's `auth.authenticate`.
    - Logs the user in if credentials are valid.
    - Redirects to the dashboard on success or back to login on failure.
    - Shows appropriate success or error messages.
    """
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

# Function for user registration
def register(request):
    """
    Handles user registration functionality.
    - Collects user data (first name, last name, username, email, password) from the POST request.
    - Validates password confirmation, username uniqueness, and email uniqueness.
    - Creates a new user if all validations pass.
    - Automatically logs the user in after successful registration.
    - Redirects to the dashboard on success or back to registration on failure.
    - Shows appropriate success or error messages.
    """
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


# Function for user dashboard
@login_required(login_url = 'login')
def dashboard(request):
    """
    Displays the user dashboard.
    - Shows inquiries made by the logged-in user, ordered by the creation date.
    - Ensures that only logged-in users can access this view.
    - Redirects unauthenticated users to the login page.
    """
    user_inquiry = Contact.objects.order_by('-create_date').filter(user_id=request.user.id)
    data = {
        'inquiries': user_inquiry,
    }
    return render(request, 'accounts/dashboard.html', data)

# Function for user logout
def logout(request):
    """
    Handles user logout functionality.
    - Logs out the current user when a POST request is received.
    - Redirects to the home page after logging out.
    - Ensures only POST requests trigger the logout process for security.
    """
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
    return redirect('home')
