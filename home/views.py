from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from .models import Expenses, Splitmembers, Splits, Splittransactions
from datetime import datetime

@login_required
def index(request):
    user = request.user
    current_month = datetime.now().strftime('%m')
    current_year = datetime.now().strftime('%Y')
    showing_month = datetime.now().strftime('%B, %Y')
    userobj = User.objects.get(username=user.username)
    years = Expenses.objects.dates('datespent','year')
    years_list = []
    for year in years:
        years_list.append(year.strftime('%Y'))
    if request.method == 'GET':
        query_year = request.GET.get('year',current_year)
        query_month = request.GET.get('month',current_month)
        showing_month = datetime(int(query_year),int(query_month),1).strftime('%B, %Y')
        query_month_expenses = Expenses.objects.filter(datespent__year=query_year,datespent__month=query_month, username=userobj)
        query_month_expenses_total = query_month_expenses.aggregate(Sum('amount'))
        context = {
            'username':user.username,
            'expenses':query_month_expenses,
            'month_total': query_month_expenses_total['amount__sum'],
            'years_list': years_list,
            'showing_month': showing_month,
            'qyear': query_year,
            'month': int(query_month)
            }
        return render(request, 'home/index.html',context)
    this_month_expenses = Expenses.objects.filter(datespent__month=current_month, username=userobj)
    this_month_expenses_total = Expenses.objects.filter(datespent__month=current_month, username=userobj).aggregate(Sum('amount'))
    context = {
        'username':user.username,
        'expenses':this_month_expenses,
        'month_total': this_month_expenses_total['amount__sum'],
        'years_list': years_list,
        'showing_month': showing_month
        }
    return render(request, 'home/index.html',context)

@login_required
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

@login_required
def deleteexpense(request):
    pk = request.GET.get('id')
    expenseobj = Expenses.objects.get(id=pk).delete()
    return redirect('index')


@login_required
def createsplit(request):
    user = request.user
    userobj = User.objects.get(username=user.username)
    groups = Splitmembers.objects.filter(member_id=userobj.id)
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
        context = {'username':user.username,'groups':groups}
        return render(request, 'home/createsplit.html', context=context)

@login_required
def managesplits(request,pk):
    user = request.user
    members = []
    userobj = User.objects.get(username=user.username)
    splitobj = Splits.objects.get(id=pk)
    splitmemberobj = Splitmembers.objects.filter(splitid=splitobj)
    totalspendings = Splittransactions.objects.filter(splitid=splitobj,spentby_id=userobj.id).aggregate(Sum('amount'))
    transactions1 = Splittransactions.objects.filter(splitid=splitobj,mode='O')
    amount_members = {}
    for member in splitmemberobj:
        if userobj.id != member.member_id:
            amount_spentbyuser = transactions1.filter(spentby_id=userobj.id,spentfor_id=member.member_id).aggregate(Sum('amount'))
            amount_spentforuser = transactions1.filter(spentby_id=member.member_id,spentfor_id=userobj.id).aggregate(Sum('amount'))
            print(amount_spentbyuser,amount_spentforuser)
            if amount_spentbyuser['amount__sum'] == None:
                amount_spentbyuser['amount__sum'] = 0
            if amount_spentforuser['amount__sum'] == None:
                amount_spentforuser['amount__sum'] = 0
            balance = amount_spentbyuser['amount__sum'] - amount_spentforuser['amount__sum']
            amount_members[member.member] = balance
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
        context = {'username':user.username,'id':pk,'members':members,'amount': amount_members,
        'totalspendings':totalspendings['amount__sum']}
        return render(request, 'home/managesplits.html',context=context)

@login_required
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

@login_required
def addsplittrans(request,pk):
    user = request.user
    userobj = User.objects.get(username=user.username)
    splitobj = Splits.objects.get(id=pk)
    splitmemberobj = Splitmembers.objects.filter(splitid=splitobj)
    totalspendings = Splittransactions.objects.filter(splitid=splitobj,spentby_id=userobj.id).aggregate(Sum('amount'))
    transactions1 = Splittransactions.objects.filter(splitid=splitobj,mode='O')
    amount_members = {}
    for member in splitmemberobj:
        if userobj.id != member.member_id:
            amount_spentbyuser = transactions1.filter(spentby_id=userobj.id,spentfor_id=member.member_id).aggregate(Sum('amount'))
            amount_spentforuser = transactions1.filter(spentby_id=member.member_id,spentfor_id=userobj.id).aggregate(Sum('amount'))
            print(amount_spentbyuser,amount_spentforuser)
            if amount_spentbyuser['amount__sum'] == None:
                amount_spentbyuser['amount__sum'] = 0
            if amount_spentforuser['amount__sum'] == None:
                amount_spentforuser['amount__sum'] = 0
            balance = amount_spentbyuser['amount__sum'] - amount_spentforuser['amount__sum']
            amount_members[member.member] = balance
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
            mode = ''
            if userobj.id == memberobj.id:
                mode = 'S'
            else:
                mode = 'O'
            splittransobj = Splittransactions(splitid=splitobj, spentby=userobj, spentfor=memberobj, amount=each_amount, spentat=purpose, datespent=datetime.now().strftime('%Y-%m-%d'), mode=mode)
            splittransobj.save()
        messages.add_message(request, messages.INFO, "Your transaction has been saved")
        return redirect('addsplittrans',pk)
    splittransobj = Splittransactions.objects.filter(splitid=splitobj)
    print(amount_members)
    context = {
        'members':splitmemberobj,
        'splittransactions':splittransobj,
        'id': pk,
        'amount': amount_members,
        'totalspendings':totalspendings['amount__sum']
        }
    return render(request,'home/addsplittrans.html',context)

@login_required
def deletesplittrans(request):
    pk = request.GET.get('id')
    splitid = request.GET.get('splitid')
    print(pk,splitid)
    Splittransactions.objects.get(id=pk).delete()
    splittransobj = Splittransactions.objects.filter(splitid_id=splitid)
    context = {'splittransactions':splittransobj}
    return render(request,'home/deletesplittrans.html',context)
    
