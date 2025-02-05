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

    def generateID(self):
        y=hashlib.sha256(str(self.id).encode()).hexdigest()
        self.unique_id=y
    
    