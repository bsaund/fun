import sha3 # pysha3, not sha3
import ecdsa
import secrets
from multiprocessing import Process
import os

PRINTLIMIT=1000000

interesting_keys = \
    [
        "71f74f5aeae759384c4b458ec36b317a98bbc5d20f165a7ab2608c0c3edfef7e06f77788f317fb08adedb944f41b8854acba5c13088c65117bcfa234bf98c9a2",
        # mine
        "bc7ab3ba9a723184126aec5888090b26f144cdcce5a7c8877bed1da5f421a94dcff7554bb2809c8abc1db17d0d424d61c90cc6cfba72e49db7864f181b19382c",
        "e9aa7ed9d74b0f5c039b8350a477b9484dc0dc0f35eea9d11c9ac0b9511155f92c12133d14bafd6a565f96ef2f2a5368ac002cea248d1052f09040fcc968aa04",
        "79015df7da6c3db4d86efb17c59ba03ed6b75e0f2fe694522d90038bf4b089d3cb47852097c8f24ff6e7dc6ef6d8ba7ec041d17ad9dca2166ac280492ab2fee3",
        "597acf4af2c1bfbd2612d35f83d5829ff142bcdc99c47938400481ae4269be5be3794f57c2ece3a5d4b5974ba9e8f975cb3657a6ca53b0dc9b882c1d011c733f",
        "c6f8c5d97f11abf95c95e730071a9323b0bc1803d379be5f3f8ee05c0b1ed6e1e9285753ec1d7fc51a139d95c9c79b32ce58d4ebf086cdca94d6d2def88a4d35",
        "8f5705baed257e99afba180b61201ea54ada2d77df805d98bb8c433bfa128a969f5874bd307ab1da38ac1a670f96a516d03037899bc24262ce6712b8876f3547",
        "f539b2b18ac94c5ab83aca14cee90b58bad2f79586f25b9cf5fb44bd7256b007a5c66349a237c37460284f1d0a1cd7dbbf0935a4577b99b232f067721268bb4f",
        "96e0985b97c889b527e11b27e7330f3cd2b879b1354add756c454aac7524dc141ccac9c1821b7fb214e1561f56db7f2ab93b3eb2ae7713d310c8ec829807e0a0",
    ]

keccak = sha3.keccak_256()


def address_formatted(to_hash_str):
    # keccak = sha3.keccak_256()
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


def private_to_account(private_key_hex):
    private_key_hex_nopad = private_key_hex[2:]
    private_key = bytearray.fromhex(private_key_hex_nopad)
    # f = hex(int(private_key_str, base=16))
    private_key = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    public_key = private_key.get_verifying_key().to_string()
    keccak.update(public_key)
    return public_key.hex()


def padhexa(s):
    return '0x' + s[2:].zfill(64)


def endless_search():
    i = 0
    while True:
        i += 1
        private_key_hex = hex(int(bin(secrets.randbits(256)), base=2))
        private_key_hex = padhexa(private_key_hex)
        if len(private_key_hex) != 66:
            print(private_key_hex)
        # print(f"checking key {private_key_hex}")
        if check_key(private_key_hex):
            return
        if i % PRINTLIMIT == 0:
            print(f"Process {os.getpid()} Checked {int(i / PRINTLIMIT)} million keys")


def check_key(private_key_hex):
    public = private_to_account(private_key_hex)
    if public in interesting_keys:
        print(f"Found private key! {private_key_hex} that matches {public}")
        with open("./found_keys.txt", 'a') as f:
            f.write(private_key_hex)
            f.write("\n")
            f.write(public)
            f.write("\n\n")
        print("!!!!!!!!!!!!!!!!!!!!!")
        return True
    return False


# endless_search()
if __name__ == "__main__":
    processes = []
    for i in range(10):
        processes.append(Process(target=endless_search))
        processes[-1].start()
