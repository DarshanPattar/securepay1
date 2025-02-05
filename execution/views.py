from django.shortcuts import render, redirect
from .models import Member
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
    return render(request,'proposer.html')

def receive(request):
    return render(request,'receiver.html')

def accept_propose(request):
    return render(request,'propose-confirm.html')

def login(request):
    return render(request,'login.html')
