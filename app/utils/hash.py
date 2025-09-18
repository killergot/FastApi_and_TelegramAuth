from hashlib import sha256

def get_hash(data: any) -> str:
    data = str(data)
    return sha256(data.encode()).hexdigest()