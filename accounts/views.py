from django.contrib import messages, auth
from django.shortcuts import render, redirect
from django.core.validators import validate_email
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import FormContact


def login(request):
    if request.method != 'POST':
        return render(request, 'accounts/login.html')

    user = request.POST.get('user')
    password = request.POST.get('password')

    user_auth = auth.authenticate(request, username=user, password=password)
    print(user_auth)
    if not user_auth:
        messages.error(request, 'User or password is invalid.')
        return render(request, 'accounts/login.html')
    else:
        auth.login(request, user_auth)
        messages.success(request, 'You are logged!')
        return redirect('dashboard')


def logout(request):
    auth.logout(request)
    return redirect('login')


def register(request):
    if request.method != 'POST':
        return render(request, 'accounts/register.html')
    name = request.POST.get('name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    user = request.POST.get('user')
    password = request.POST.get('password')
    confirmPassword = request.POST.get('confirmPassword')

    if not name or not last_name or not email or not user or not password or not confirmPassword:
        messages.error(request, 'Fill all fields')
        return render(request, 'accounts/register.html')

    try:
        validate_email(email)
    except:
        messages.error(request, 'Email is invalid')
        return render(request, 'accounts/register.html')

    if len(password) < 6:
        messages.error(request, 'The password must have 6 characters at least.')
        return render(request, 'accounts/register.html')

    if len(user) < 6:
        messages.error(request, 'The user must have 6 characters at least.')
        return render(request, 'accounts/register.html')

    if password != confirmPassword:
        messages.error(request, "The confirm password doesn't match with password.")
        return render(request, 'accounts/register.html')

    if User.objects.filter(username=user).exists():
        messages.error(request, "There is a user with this username")
        return render(request, 'accounts/register.html')

    if User.objects.filter(email=email).exists():
        messages.error(request, "There is a user with this email")
        return render(request, 'accounts/register.html')

    user = User.objects.create_user(
        username=user,
        email=email,
        first_name=name,
        last_name=last_name,
        password=password
    )

    user.save()

    messages.success(request, "User registered with success!")
    return redirect('login')


@login_required(redirect_field_name='login')
def dashboard(request):
    if request.method != 'POST':
        form = FormContact()
        return render(request, 'accounts/dashboard.html', {'form': form})

    form = FormContact(request.POST, request.FILES)

    if not form.is_valid():
        messages.error(request, 'Error to submit form')
        form = FormContact(request.POST)
        return render(request, 'accounts/dashboard.html', {'form': form})

    form.save()
    messages.success(request, f'Contact {request.POST.get("name")} saved with success!')
    return redirect('dashboard')
