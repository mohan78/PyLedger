from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Expenses, Splitmembers, Splits, Splittransactions
from datetime import datetime

def index(request):
    user = request.user
    month = datetime.now().strftime('%m')
    userobj = User.objects.get(username=user.username)
    this_month_expenses = Expenses.objects.filter(datespent__month=month, username=userobj)
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
        splitmemberobj = Splitmembers(splitid=splitobj,member=userobj)
        splitmemberobj.save()
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
        try:
            memberobj = User.objects.get(username=member)
        except User.DoesNotExist:
            messages.add_message(request, messages.INFO, "Username not found")
            return redirect('managesplits',pk)
        if Splitmembers.objects.filter(splitid=splitobj,member=memberobj).exists():
            messages.add_message(request, messages.INFO, "Member already exists")
            return redirect('managesplits',pk)
        obj = Splitmembers(splitid=splitobj, member=memberobj)
        obj.save()
        return redirect('managesplits',pk)
    else:
        context = {'username':user.username,'id':pk,'members':members}
        return render(request, 'home/managesplits.html',context=context)

def deletemember(request):
    username = request.GET.get('username')
    splitid = request.GET.get('splitid')
    members = []
    userobj = User.objects.get(username=username)
    splitobj = Splits.objects.get(id=splitid)
    Splitmembers.objects.filter(member=userobj, splitid=splitobj).delete()
    splitmemberobj = Splitmembers.objects.filter(splitid=splitid)
    for splitmember in splitmemberobj:
        memberobj = User.objects.get(id=splitmember.member.id)
        members.append(memberobj)
    context = {'members':members}
    return render(request,'home/deletemembers.html',context)

def addsplittrans(request,pk):
    user = request.user
    userobj = User.objects.get(username=user.username)
    splitobj = Splits.objects.get(id=pk)
    splitmemberobj = Splitmembers.objects.filter(splitid=splitobj)
    amount_spent_obj = Splittransactions.objects.filter(splitid=splitobj, spentby=userobj)
    amount_spent = 0
    amount_payable_obj = Splittransactions.objects.filter(splitid=splitobj, spentfor=userobj)
    amount_payable = 0
    amount_payable_others_obj = Splittransactions.objects.filter(splitid=splitobj,spentfor=userobj).exclude(spentby=userobj)
    amount_payable_others = 0
    for item in amount_spent_obj:
        amount_spent += int(item.amount)
    for item in amount_payable_obj:
        amount_payable += int(item.amount)
    for item in amount_payable_others_obj:
        amount_payable_others += int(item.amount)
    print(amount_spent, amount_payable_others, amount_spent-amount_payable)
    if request.method == 'POST':
        purpose = request.POST.get('purpose')
        amount = request.POST.get('amount','0')
        members = request.POST.getlist('membername')
        if int(amount) < 0:
            messages.add_message(request, messages.INFO, 'Please enter an valid amount')
            return redirect('addsplittrans',pk)
        each_amount = int(amount)/len(members)
        for member in members:
            memberobj = User.objects.get(username=member)
            splittransobj = Splittransactions(splitid=splitobj, spentby=userobj, spentfor=memberobj, amount=each_amount, spentat=purpose, datespent=datetime.now().strftime('%Y-%m-%d'))
            splittransobj.save()
        messages.add_message(request, messages.INFO, "Your transaction has been saved")
        return redirect('addsplittrans',pk)
    splittransobj = Splittransactions.objects.filter(splitid=splitobj)
    context = {
        'members':splitmemberobj,
        'splittransactions':splittransobj,
        'amount_spent': amount_spent,
        'amount_payable_others':amount_payable_others,
        'amount_receivables': amount_spent - amount_payable
        }
    return render(request,'home/addsplittrans.html',context)

