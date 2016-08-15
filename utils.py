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

def whether_compressed_privatekey(privatekey):
    private_key_decode = base58.b58decode_check(privatekey)
    if len(private_key_decode) ==33:
        return False
    elif len(private_key_decode) ==34:
        return True

def whether_bitcoinaddress(bitcoinaddress):
    try:
        private_key_decode = base58.b58decode_check(bitcoinaddress)
        return True
    except:
        return False

def int_to_32hex(number):
    assert isinstance(number, int) and number>0, 'number must be positive integer'
    str_bin = bin(number)[2:].rjust(256, '0')
    hex_privatekey = bytes([int(str_bin[x*8:x*8+8], 2) for x in range(32)])
    return hex_privatekey

def int_to_privatekey(number):
    assert isinstance(number, int) and number>0, 'number must be positive integer'
    uncompressed = base58.b58encode_check(b'\x80'+int_to_32hex(number))
    compressed = base58.b58encode_check(b'\x80'+int_to_32hex(number)+b'\x01')
    return uncompressed, compressed

def privatekey_to_int(privatekey):
    if whether_compressed_privatekey(privatekey):
        hex32private = base58.b58decode_check(privatekey)[1:-1]
    else:
        hex32private = base58.b58decode_check(privatekey)[1:]
    str_bin = ''.join([bin(x)[2:].rjust(8, '0') for x in hex32private])
    number = int(str_bin,2)
    return number
