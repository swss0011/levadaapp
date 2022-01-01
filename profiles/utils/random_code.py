import secrets

def get_code():
    return secrets.token_hex(64)