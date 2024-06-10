from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def login_page(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, 'Invalid Username!')
            return redirect('login_page')
        
        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, 'Invalid Password!')
            return redirect('login_page')
        else:
            login(request, user)
            return redirect('all-trade')
    
    return render(request, 'users/login.html')


def register_page(request):

    if request.method == 'POST':

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username = username)

        if user.exists():
            messages.info(request, 'Username Already Taken!')
            return redirect('register')
        
        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username
        )

        user.set_password(password)
        user.save()
        
        user = authenticate(username=username, password=password)
        login(request, user)

        # messages.info(request, "Account Created Successfully!")
        return redirect('all-trade')

    return render(request, 'users/register.html')


def logout_page(request):
    logout(request)
    # messages.info(request, "You have logged out seccessfully!")
    return redirect('all-trade')