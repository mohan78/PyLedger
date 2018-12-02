from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Expenses, Splitmembers, Splits, Splittransactions
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

def createsplit(request):
    user = request.user
    if request.method == 'POST':
        name = request.POST.get('groupname')
        userobj = User.objects.get(username=user.username)
        datecreated = datetime.now().strftime('%Y-%m-%d')
        splitobj = Splits(username=userobj, name=name, datecreated=datecreated)
        splitobj.save()
        return redirect('managesplits',splitobj.id)
    else:
        context = {'username':user.username}
        return render(request, 'home/createsplit.html', context=context)

def managesplits(request,pk):
    user = request.user
    members = []
    splitmemberobj = Splitmembers.objects.filter(splitid=pk)
    for splitmember in splitmemberobj:
        memberobj = User.objects.get(id=splitmember.member.id)
        members.append(memberobj)
    if request.method == 'POST':
        splitobj = Splits.objects.get(id=pk)
        member = request.POST.get('username')
        memberobj = User.objects.get(username=member)
        if Splitmembers.objects.filter(member=memberobj).exists():
            messages.add_message(request, messages.INFO, "Member already exists")
            return redirect('managesplits',pk)
        obj = Splitmembers(splitid=splitobj, member=memberobj)
        obj.save()
        return redirect('managesplits',pk)
    else:
        context = {'username':user.username,'id':pk,'members':members}
        return render(request, 'home/managesplits.html',context=context)

def addsplittrans(request):
    pass