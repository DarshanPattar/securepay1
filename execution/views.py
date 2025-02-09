from django.shortcuts import render, redirect, HttpResponse
from .models import *
from .IntegrityManager import *
import json
from datetime import datetime
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
        #create a json file
        transaction_receiver={
            'id':member.id,
            'from':'cmanager',
            'to':member.unique_id,
            'amount':0,
            'transaction_hash':HashStr(str(member.id)+str('cmanager')+str(member.unique_id)+str(0)),
            'balance':member.balance,
            'balance_hash':HashStr(""),
            'time':datetime.now().isoformat()
        }
        with open('databases/'+member.unique_id+'.json','w') as f:
            f.write('{"transactions":[]}')
        with open('databases/'+member.unique_id+'.json','r+') as f:
            
            data=json.load(f)
            data['transactions'].append(transaction_receiver)
            f.seek(0)
            json.dump(data,f)
            f.truncate()
        request.session['member_id'] = member.id
        tm=Memtransactions(memid=member.unique_id,jsonpath='databases/'+member.unique_id+'.json')
        tm.save()
        return redirect('/')
    
    return render(request,'register-mem.html')

def home(request):
    if 'member_id' in request.session:
        member = Member.objects.get(id=request.session.get('member_id'))
        proposed=Proposer.objects.filter(fromid=member.unique_id)
        confirmed=Twoconfirms.objects.filter(fromid=member.unique_id)
        
        with open('databases/'+member.unique_id+'.json','r+') as f:
            data=json.load(f)
        transactions=data['transactions']
        balHash = transactions[-1]['balance_hash']
        return render(request,'home.html', context={'member':member,'proposed':proposed,'confirmed':confirmed,'transactions':transactions, 'balHash':balHash})
    else:
        return redirect('register')



#Delete all members
def delmem(request):
    Member.objects.all().delete()
    Cmanager.objects.all().delete()
    Proposer.objects.all().delete()
    Twoconfirms.objects.all().delete()
    Memtransactions.objects.all().delete()
    
    return redirect('/')

def logout(request):
    request.session.flush()
    return redirect('register')

#Propose new transaction
def propose(request):
    ob=Member.objects.get(id=request.session.get('member_id'))
    if request.method=='POST':
        
        fromid=ob.unique_id
        fname=ob.unique_name
        toid=request.POST['toid']
        toname=request.POST['toname']
        amount=request.POST['amount']
        proposer=Proposer(fromid=fromid,fname=fname,toidd=toid,toname=toname,amount=amount)
        proposer.save()
    obj=Member.objects.all()
    return render(request,'proposer.html',context={'ob':ob,'member':obj})

def receive(request):
    return render(request,'receiver.html')

#Accepting the transaction
def accept_propose(request,id):
    if request.method=='POST':
        ob=Proposer.objects.get(id=id)
        passw = request.POST['st']
        receiver=Member.objects.get(id = request.session.get('member_id'))
        if receiver.password==passw:
            ob.status='accepted'
            ob.save()
            succobj=Twoconfirms(fromid=ob.fromid,toid=ob.toidd,amount=ob.amount)
            succobj.save()
            if(ValidateTrans(succobj)):
                succobj.imanagerstatus='accepted'
                succobj.save()
                receiver.balance+=ob.amount
                receiver.save()
                sender=Member.objects.get(unique_id = ob.fromid)
                sender.balance-=ob.amount
                sender.save()
                primitivestr = str(succobj.id)+str(succobj.fromid)+str(succobj.toid)+str(succobj.amount)
                transaction_id_hash=hashlib.shake_256(str(primitivestr).encode()).hexdigest(5)
                sender_merkle=create_merkle(extract(sender.unique_id))
                receiver_merkle=create_merkle(extract(receiver.unique_id))
                tms=Memtransactions.objects.get(memid=sender.unique_id)
                tms.merkleroot=sender_merkle
                tms.save()
                tmr=Memtransactions.objects.get(memid=receiver.unique_id)
                tmr.merkleroot=receiver_merkle
                tmr.save()
                with open('databases/'+receiver.unique_id+'.json','r+') as f:
                    data=json.load(f)
                    transaction_receiver={
                        'id':succobj.id,
                        'from':ob.fromid,
                        'to':ob.toidd,
                        'amount':ob.amount,
                        'transaction_hash':transaction_id_hash,
                        'balance':receiver.balance,
                        'balance_hash':HashStr(str(data['transactions'][-1]['balance_hash'])+str(receiver.balance)),
                        'merkleroot':tms.merkleroot,
                        'time':datetime.now().isoformat(),
                    }
                    data['transactions'].append(transaction_receiver)
                    f.seek(0)
                    json.dump(data,f)
                    f.truncate()
                with open('databases/'+sender.unique_id+'.json','r+') as f:
                    data=json.load(f)
                    transaction_sender={
                        'id':succobj.id,
                        'from':ob.fromid,
                        'to':ob.toidd,
                        'amount':ob.amount,
                        'transaction_hash':transaction_id_hash,
                        'balance':sender.balance,
                        'balance_hash':HashStr(str(data['transactions'][-1]['balance_hash'])+str(sender.balance)),
                        'merkleroot':tmr.merkleroot,
                        'time':datetime.now().isoformat()
                    }
                    data['transactions'].append(transaction_sender)
                    f.seek(0)
                    json.dump(data,f)
                    f.truncate()
                sender_merkle=create_merkle(extract(sender.unique_id))
                receiver_merkle=create_merkle(extract(receiver.unique_id))
                tms=Memtransactions.objects.get(memid=sender.unique_id)
                tms.merkleroot=sender_merkle
                tms.save()
                tmr=Memtransactions.objects.get(memid=receiver.unique_id)
                tmr.merkleroot=receiver_merkle
                tmr.save()
            else:
                succobj.imanagerstatus='rejected'
                succobj.save()
            return redirect('/')
        else:
            return HttpResponse('Invalid password')

    ob=Proposer.objects.get(id=id)
    return render(request,'receiver.html',context={'ob':ob})



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
    member=Member.objects.get(id = request.session.get('member_id'))
    if request.method=='POST':
        memid=member.unique_id
        memname=member.unique_name
        amount=request.POST['reqc']
        cmanager=Cmanager(memid=memid,memname=memname,amount=amount)
        ob=Member.objects.get(unique_id=memid)
        ob.balance=ob.balance+int(amount)    
        ob.save()
        cmanager.save()
        with open('databases/'+ob.unique_id+'.json','r+') as f:
            data=json.load(f)
            transaction_receiver={
                'id':ob.id,
                'from':'cmanager',
                'to':ob.unique_id,
                'amount':amount,
                'transaction_hash':HashStr(str(ob.id)+str('cmanager')+str(ob.unique_id)+str(amount)),
                'balance':ob.balance,
                'balance_hash':HashStr(str(data['transactions'][-1]['balance_hash'])+str(ob.balance))
            }
            data['transactions'].append(transaction_receiver)
            f.seek(0)
            json.dump(data,f)
            f.truncate()
    return render(request,'cmanager.html',context={'member':member})


def transaction_notifications(request):
    member=Member.objects.get(id = request.session.get('member_id'))
    transactions = Proposer.objects.filter(toidd=member.unique_id)
    print(request.session.get('member_id'))
    print(Proposer.objects.all())
    if not transactions:
        return redirect('/')
    context = {'tr':transactions}
    return render(request,'reciever_notification.html', context)


