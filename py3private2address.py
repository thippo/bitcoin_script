#Reference: https://github.com/sarchar/addressgen
#Thanks!

import base58
import ctypes
import hashlib

try:
    ssl_library = ctypes.cdll.LoadLibrary('libeay32.dll')
except:
    ssl_library = ctypes.cdll.LoadLibrary('libssl.so')

class Private2Address():

    def __init__(self, private_key):
        self.private_key = private_key
        self.NID_secp256k1 = 714
        self.bitcoinaddress_uncompress,self.bitcoinaddress_compress = self._get_bitcoin_address()

    def _get_public_key(self, private_key, curve_name):
        k = ssl_library.EC_KEY_new_by_curve_name(curve_name)
        storage = ctypes.create_string_buffer(private_key)
        bignum_private_key = ssl_library.BN_new()
        ssl_library.BN_bin2bn(storage, 32, bignum_private_key)
        group = ssl_library.EC_KEY_get0_group(k)
        point = ssl_library.EC_POINT_new(group)
        ssl_library.EC_POINT_mul(group, point, bignum_private_key, None, None, None)
        ssl_library.EC_KEY_set_private_key(k, bignum_private_key)
        ssl_library.EC_KEY_set_public_key(k, point)
        size = ssl_library.i2o_ECPublicKey(k, 0)
        storage = ctypes.create_string_buffer(size)
        pstorage = ctypes.pointer(storage)
        ssl_library.i2o_ECPublicKey(k, ctypes.byref(pstorage))
        public_key_uncompress = storage.raw
        ssl_library.EC_POINT_free(point)
        ssl_library.BN_free(bignum_private_key)
        ssl_library.EC_KEY_free(k)
        return public_key_uncompress, self._compress(public_key_uncompress)

    def _compress(self, public_key_uncompress):
        x_coord = public_key_uncompress[1:33]
        if public_key_uncompress[64] & 0x01:
            c = bytes([0x03]) + x_coord
        else:
            c = bytes([0x02]) + x_coord
        return c

    def _sha256ripemd160(self, public_key):
        hasher = hashlib.sha256()
        hasher.update(public_key)
        hasher = hasher.digest()
        hasher2 = hashlib.new('ripemd160')
        hasher2.update(hasher)
        hasher2 = hasher2.digest()
        return hasher2

    def _get_bitcoin_address(self):
        private_key_decode = base58.b58decode_check(self.private_key)
        if len(private_key_decode) ==33:
            private_key = private_key_decode[1:]
        elif len(private_key_decode) ==34:
            private_key = private_key_decode[1:-1]
        else:
            raise Exception
        public_key_uncompress,public_key_compress = self._get_public_key(private_key, self.NID_secp256k1)
        return base58.b58encode_check(b'\x00'+self._sha256ripemd160(public_key_uncompress)), base58.b58encode_check(b'\x00'+self._sha256ripemd160(public_key_compress))

if __name__ == '__main__':
    p2a=Private2Address('5HpHagT65TZzG1PH3CSu63k8DbpvD8s5ip4nEB3kEsreAnchuDf')
    print(p2a.bitcoinaddress_uncompress, p2a.bitcoinaddress_compress)