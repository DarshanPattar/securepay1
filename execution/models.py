from django.db import models
import random
import hashlib
# Create your models here.
class Member(models.Model):
    cho=[('upto10k','10k'),('abovetill100k','10kTo100k')]
    name=models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    affiliation=models.CharField(max_length=100)
    unique_name=models.CharField(max_length=100, unique=True)
    unique_id=models.CharField(max_length=256)
    category=models.CharField(max_length=100,choices=cho,default='upto10k')
    password=models.CharField(max_length=100)
    balance=models.IntegerField(default=0)
    intransaction=models.IntegerField(default=0)
    def generateID(self):
        y=hashlib.shake_256(str(self.id).encode()).hexdigest(5)
        self.unique_id=y
    
class Proposer(models.Model):
    ch=[('pending','pending'),('accepted','accepted'),('rejected','rejected')]
    fromid=models.CharField(max_length=256)
    fname=models.CharField(max_length=100)
    toidd=models.CharField(max_length=256)
    toname=models.CharField(max_length=100)
    amount=models.IntegerField()
    status=models.CharField(max_length=100,choices=ch,default='pending')

class Twoconfirms(models.Model):
    ch=[('pending','pending'),('accepted','accepted'),('rejected','rejected')]
    fromid=models.CharField(max_length=256)
    toid=models.CharField(max_length=256)
    amount=models.IntegerField()
    imanagerstatus=models.CharField(max_length=100,choices=ch,default='pending')

class Cmanager(models.Model):
    memid=models.CharField(max_length=256)
    memname=models.CharField(max_length=100)
    amount=models.IntegerField()

class Memtransactions(models.Model):
    memid=models.CharField(max_length=256)
    merkleroot=models.CharField(max_length=256)
    jsonpath=models.CharField(max_length=256)