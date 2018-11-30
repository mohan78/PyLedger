from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from home.views import index

def register(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.add_message(request,messages.INFO,"Username already exists, please choose another.")
            return redirect('signup')
        if User.objects.filter(email=email).exists():
            messages.add_message(request,messages.INFO,"Email already in use, please login")
            return redirect('signup')
        userobj = User.objects.create_user(username,email=email,password=password,first_name=firstname,last_name=lastname)
        userobj.save()
        user = authenticate(username=username,password=password)
        if user.is_authenticated:
            login(request,user)
            return redirect('index')
    else:
        return render(request,'registration/signup.html')
