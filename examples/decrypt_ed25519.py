#!/usr/bin/python3

import sys
import libsodium

def write_bytes(fname, data):
    with open(fname, 'wb') as outfile:
        outfile.write(data)
    
def read_bytes(fname):
    with open(fname, 'rb') as infile:
        data = infile.read()
    return data


def decrypt(message, shared_key):
    '''
    Decrypt data using Curve25519 with crypto_box_open_easy and a pre-calculated shared key.
    For more information: https://download.libsodium.org/doc/public-key_cryptography/authenticated_encryption.html
    '''
    # Separate nonce and ciphertext
    nonce = message[:libsodium.crypto_box_NONCEBYTES]
    ciphertext = message[libsodium.crypto_box_NONCEBYTES:]
    # Decrypt data
    plaintext = libsodium.crypto_box_open_easy_afternm(ciphertext, nonce, shared_key)
    return plaintext;


# Get input/output files from commandline

if len(sys.argv) < 3 or sys.argv[1] in ('-h', '--help'):
    print("Usage:", sys.argv[0], "<ed25519 receiver secret> <ed25519 sender pubkey> [<encrypted input file> [<decrypted output file>]]\n")
    exit()


# Load Ed25519 keyfiles

receiver_secret_ed25519 = read_bytes(sys.argv[1])
sender_pubkey_ed25519 = read_bytes(sys.argv[2])

# Convert to Curve25519-keys, see https://download.libsodium.org/doc/advanced/ed25519-curve25519.html

receiver_secret_curve = libsodium.crypto_sign_ed25519_sk_to_curve25519(receiver_secret_ed25519)
sender_pubkey_curve = libsodium.crypto_sign_ed25519_pk_to_curve25519(sender_pubkey_ed25519)

# Calculate shared key, see https://download.libsodium.org/doc/public-key_cryptography/authenticated_encryption.html

shared_key = libsodium.crypto_box_beforenm(sender_pubkey_curve, receiver_secret_curve)


# Read message to be decrypted (from file or stdin)

if len(sys.argv) >= 4:
    message = read_bytes(sys.argv[3])
else:
    message = sys.stdin.buffer.read()
    

# Try to decrypt message and write to output

try:
    plaintext = decrypt(message, shared_key)
except:
    print("Could not decrypt message\n", file=sys.stderr)
    exit(1)

if len(sys.argv) >= 5:
    write_bytes(sys.argv[4], plaintext)
else:
    sys.stdout.buffer.write(plaintext)
