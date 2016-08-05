import base58

def WIF_to_compressed(privatekey_WIF):
    return base58.b58encode_check(base58.b58decode_check(privatekey_WIF)+b'\x01')
