from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Expenses
from datetime import datetime

def index(request):
    user = request.user
    month = datetime.now().strftime('%m')
    this_month_expenses = Expenses.objects.filter(datespent__month=month)
    context = {'username':user.username,'expenses':this_month_expenses}
    return render(request, 'home/index.html',context)

def addexpense(request):
    user = request.user
    userobj = User.objects.get(username=user.username)
    if request.method == 'POST':
        category = request.POST.get('category')
        spentat = request.POST.get('spentat')
        amount = request.POST.get('amount')
        modeofpayment = request.POST.get('modeofpayment')
        datespent = request.POST.get('datespent')
        print(category)
        if int(amount) < 0:
            messages.add_message(request, messages.INFO, 'Please enter an valid amount')
            return redirect('addexpense')
        else:
            trasaction = Expenses(category=category,spentat=spentat,amount=amount,modeofpayment=modeofpayment,datespent=datespent,username=userobj)
            trasaction.save()
            messages.add_message(request, messages.INFO, 'Your expense record has been saved')
            return redirect('addexpense')
    context = {'username':user.username}
    return render(request, 'home/addexpense.html', context)
