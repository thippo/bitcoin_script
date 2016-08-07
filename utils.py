import base58

def WIF_to_compressed(privatekey_WIF):
    return base58.b58encode_check(base58.b58decode_check(privatekey_WIF)+b'\x01')

def compressed_to_WIF(privatekey_compressed):
    return base58.b58encode_check(base58.b58decode_check(privatekey_compressed)[:-1])

def whether_privatekey(privatekey):
    try:
        private_key_decode = base58.b58decode_check(privatekey)
        return True
    except:
        return False

def whether_compressed(privatekey):
    private_key_decode = base58.b58decode_check(privatekey)
    if len(private_key_decode) ==33:
        return False
    elif len(private_key_decode) ==34:
        return True
