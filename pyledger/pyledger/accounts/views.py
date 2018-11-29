from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from home.views import index

def register(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        userobj = User.objects.create_user(username,email=email,password=password,first_name=firstname,last_name=lastname)
        userobj.save()
        user = authenticate(username=username,password=password)
        if user.is_authenticated:
            login(request,user)
            return redirect('index')
    else:
        return render(request,'registration/signup.html')
