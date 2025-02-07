import hashlib

def HashStr(stri):
    return hashlib.shake_256(str(stri).encode()).hexdigest(5)

print(HashStr('46b9dd2b0b'+'50'))