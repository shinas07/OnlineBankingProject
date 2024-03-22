from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth import logout as auth_logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
import re
from django.views.decorators.cache import never_cache


@never_cache
def register_user(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not username or username.strip() == "":
            messages.error(request, "Username cannot be empty")
        elif len(username) < 3:
            messages.error(request,"Username must be at least 3 characters long")
        elif len(username) > 12:
            messages.error(request,"Username cannot exceed 12 character")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken")
        elif len(password) < 8:
            messages.error(request, "Password must be at least 8 characters long")
        elif not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
            messages.error(request, "Make your password stronger with uppercase, lowercase, digits, and symbols.")
        elif password != confirm_password:
            messages.error(request, "Passwords do not match")
        else:
            hashed_password = make_password(password)  
            user = User.objects.create(username=username, password=hashed_password)
            messages.success(request, "User successfully registered")
            return redirect("accounts:login")

        return render(request, "register.html")
    
    return render(request, "register.html")


@never_cache
def user_login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('new_page')
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    return render(request, 'login.html')


    
@never_cache
@login_required(login_url='home')
def logout_veiw(request):
    auth_logout(request)
    return redirect('home')