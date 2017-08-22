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

# Get input/output files from commandline

if len(sys.argv) < 3 or sys.argv[1] in ('-h', '--help'):
    print("Usage:", sys.argv[0], "<ed25519 sender pubkey> [<input signed message file> [<output message file]]\n")
    exit()


# Load Ed25519 keyfile

sender_pubkey_ed25519 = read_bytes(sys.argv[1])

# Read message to be verified

if len(sys.argv) >= 3:
    signed_message = read_bytes(sys.argv[2])
else: 
    signed_message = sys.stdin.buffer.read()

# Verify signature

try:
    message = libsodium.crypto_sign_open(signed_message, sender_pubkey_ed25519)
except:
    print("Signature does not match message\n", file=sys.stderr)
    exit(1)

print("Signature matches message\n", file=sys.stderr)

if len(sys.argv) >= 4:
    write_bytes(sys.argv[3], message)
else:
    sys.stdout.buffer.write(message)
