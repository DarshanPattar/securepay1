from django.shortcuts import render, redirect
from .models import *
# Create your views here.
def register(request):
    if request.method=='POST':
        name=request.POST['name']
        address=request.POST['address']
        affiliation=request.POST['affiliation']
        unique_name=request.POST['unique_name']
        password=request.POST['password']
    
        category=request.POST['category']
        member=Member(name=name,address=address,affiliation=affiliation,unique_name=unique_name,password=password,category=category)
        
        member.save()
        member.generateID()
        member.save()
        request.session['member_id'] = member.id
        return redirect('/')
    return render(request,'register-mem.html')

def home(request):
    if 'member_id' in request.session:
        member = Member.objects.get(id=request.session.get('member_id'))
        return render(request,'home.html', context={'member':member})
    else:
        return redirect('register')
    
def delmem(request):
    ob=Member.objects.all()
    for n in ob:
        n.delete()
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('register')

def propose(request):
    ob=Member.objects.get(id=request.session.get('member_id'))
    if request.method=='POST':
        
        fromid=ob.unique_id
        fname=ob.unique_name
        toid=request.POST['toid']
        toname=request.POST['toname']
        amount=request.POST['amount']
        proposer=Proposer(fromid=fromid,fname=fname,toid=toid,toname=toname,amount=amount)
        proposer.save()
    
    return render(request,'proposer.html',context={'ob':ob})

def receive(request):
    return render(request,'receiver.html')

def accept_propose(request):
    return render(request,'propose-confirm.html')

def login(request):
    if request.method=='POST':
        unique_name=request.POST['username']
        password=request.POST['password']
        try:
            member=Member.objects.get(unique_name=unique_name,password=password)
            request.session['member_id'] = member.id
            return redirect('/')
        except Member.DoesNotExist:
            return render(request,'login.html',{'error':'Invalid username or password'})
    return render(request,'login.html')


def cmanager(request):
    if request.method=='POST':
        memid=request.POST['memid']
        memname=request.POST['memname']
        amount=request.POST['amount']
        cmanager=Cmanager(memid=memid,memname=memname,amount=amount)
        cmanager.save()
        ob=Member.objects.get(id=memid)
        ob.balance=ob.balance+amount    
        ob.save()
    return render(request,'cmanager.html')