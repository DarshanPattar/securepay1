from .models import *


def ValidateTrans(TCO):
    sender = Member.objects.get(unique_id=TCO.fromid)
    receiver = Member.objects.get(unique_id=TCO.toid)
    amount = TCO.amount
    if sender.balance >= amount:
        return True
    return False