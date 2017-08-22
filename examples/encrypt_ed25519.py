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


def encrypt(plaintext, shared_key):
    '''
    Encrypt data using Curve25519 with crypto_box_easy and a pre-calculated shared key.
    Returns an encrypted message consisting of ciphertext appended to a random nonce.
    For more information: https://download.libsodium.org/doc/public-key_cryptography/authenticated_encryption.html
    '''
    # Generate random nonce
    nonce = libsodium.randombytes_buf(libsodium.crypto_box_NONCEBYTES)
    # Encrypt data
    ciphertext = libsodium.crypto_box_easy_afternm(plaintext, nonce, shared_key)
    # Append ciphertext to nonce
    return nonce + ciphertext;


# Get input/output files from commandline

if len(sys.argv) < 3 or sys.argv[1] in ('-h', '--help'):
    print("Usage:", sys.argv[0], "<ed25519 sender secret> <ed25519 receiver pubkey> [<input file> [<encrypted output file>]]\n")
    exit()


# Load Ed25519 keyfiles

sender_secret_ed25519 = read_bytes(sys.argv[1])
receiver_pubkey_ed25519 = read_bytes(sys.argv[2])

# Convert to Curve25519-keys, see https://download.libsodium.org/doc/advanced/ed25519-curve25519.html

sender_secret_curve = libsodium.crypto_sign_ed25519_sk_to_curve25519(sender_secret_ed25519)
receiver_pubkey_curve = libsodium.crypto_sign_ed25519_pk_to_curve25519(receiver_pubkey_ed25519)

# Calculate shared key, see https://download.libsodium.org/doc/public-key_cryptography/authenticated_encryption.html

shared_key = libsodium.crypto_box_beforenm(receiver_pubkey_curve, sender_secret_curve)


# Read plaintext to be encrypted (from file or stdin)

if len(sys.argv) >= 4:
    plaintext = read_bytes(sys.argv[3])
else:
    plaintext = sys.stdin.buffer.read()
    

# Encrypt plaintext and write to output

message = encrypt(plaintext, shared_key)

if len(sys.argv) >= 5:
    write_bytes(sys.argv[4], message)
else:
    sys.stdout.buffer.write(message)
