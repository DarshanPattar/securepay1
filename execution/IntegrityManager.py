from .models import *
from .merkle_tree import *
import json
def ValidateTrans(TCO):
    sender = Member.objects.get(unique_id=TCO.fromid)
    receiver = Member.objects.get(unique_id=TCO.toid)
    amount = TCO.amount
    if sender.balance >= amount:
        return True
    return False


def HashStr(stri):
    return hashlib.shake_256(str(stri).encode()).hexdigest(5)

def IntegrityCheck(trans):
    return trans['transaction_hash'] == HashStr(str(trans['id'])+str(trans['from'])+str(trans['to'])+str(trans['amount']))

def extract(id):
    with open('databases/'+id+'.json','r+') as f:
        data=json.load(f)
    for i in data['transactions']:
        if not IntegrityCheck(i):
            return False
    list=[]
    for i in data['transactions']:
        list.append(i['transaction_hash'])
    return list


def create_merkle(thashes):
    return MerkleTree(thashes).get_root()