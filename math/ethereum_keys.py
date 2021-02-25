import secrets
import math
import sha3
import ecdsa

# from ecdsa import SigningKey, SECP256k1
# from eth_keys import keys

private_key_hex = hex(int(input('paste a 0x-padded 64 character hex string, total 66 with 0x'), base=16))
scep256k1_curvelimit = int(0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141)  # Curve limit is
if int(private_key_hex, base=16) > scep256k1_curvelimit:
    print('private key is out of the range of the curve and invalid, do not use!')
else:
    print('private key is within range of curve')

# private_key_hex=hex(int(bin(secrets.randbits(256)),base=2)) Uncomment this to use RANDOM
private_key_hex_nopad = private_key_hex[2:]
private_key = bytearray.fromhex(private_key_hex_nopad)


def address_formatted(to_hash_str):
    keccak = sha3.keccak_256()
    out = ''
    str_hash = to_hash_str.lower().replace('0x', '')
    keccak.update(str_hash.encode('ascii'))
    create_hash_digit = keccak.hexdigest()

    for i, c in enumerate(str_hash):
        if int(create_hash_digit[i], 16) >= 8:
            out += c.upper()
        else:
            out += c
    return '0x' + out


keccak = sha3.keccak_256()
f = private_key
private_key = ecdsa.SigningKey.from_string(f, curve=ecdsa.SECP256k1)
public_key = private_key.get_verifying_key().to_string()
keccak.update(public_key)
print(public_key)
address = keccak.hexdigest()[24:]
address_full = keccak.hexdigest()

print("Private key:", private_key.to_string().hex())
print("Public key: ", public_key.hex())
print("Ethereum Address, based on last 40 hex of Keccak Hash digest:    ", address_formatted(address))
print('Full Hash Digest (address is last 40 characters): ', address_full, )
