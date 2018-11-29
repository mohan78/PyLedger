from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def index(request):
    user = request.user
    context = {'username':user.username}
    return render(request, 'home/index.html',context)

def addexpense(request):
    user = request.user
    if request.method == 'POST':
        messages = []
        category = request.POST.get('category')
        spentat = request.POST.get('spentat')
        amount = request.POST.get('amount')
        modeofpayment = request.POST.get('modeofpayment')
        datespent = request.POST.get('datespent')
        if amount < 0:
            messages.append('Please enter an valid amount')
            context = {'username':user.username,'messages':messages}
            return render(request, 'home/addexpense.html', context)
    context = {'username':user.username}
    return render(request, 'home/addexpense.html', context)
